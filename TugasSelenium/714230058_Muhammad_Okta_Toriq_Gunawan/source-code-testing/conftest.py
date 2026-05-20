"""Selenium E2E test configuration and shared fixtures."""

from __future__ import annotations

import json
import os
import random
import string
import time
import warnings

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

# Import utils
from tests.e2e.utils.db_helpers import DBHelper
from tests.e2e.utils.mock_drone import MockDronePublisher


# --- Configuration ---

FRONTEND_URL = os.getenv("TEST_FRONTEND_URL", "http://localhost:3000")
API_BASE_URL = os.getenv("TEST_API_URL", "http://localhost:5000")
GECKODRIVER_PATH = os.getenv("GECKODRIVER_PATH", "/tmp/geckodriver")

warnings.filterwarnings("ignore", category=DeprecationWarning)


def _generate_test_label() -> str:
    """Generate unique TEST label for data isolation."""
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"TEST-{suffix}"


# --- WebDriver Fixtures ---

@pytest.fixture(scope="session")
def geckodriver_service():
    """Provide geckodriver service path."""
    if not os.path.exists(GECKODRIVER_PATH):
        pytest.skip(f"geckodriver not found at {GECKODRIVER_PATH}")
    return FirefoxService(executable_path=GECKODRIVER_PATH)


@pytest.fixture(scope="function")
def driver(geckodriver_service):
    """Create a headless Firefox WebDriver per test function."""
    options = FirefoxOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Reduce logs
    options.set_preference("devtools.console.stdout.content", False)
    options.set_preference("browser.download.start_downloads_in_tmp_dir", True)

    driver = webdriver.Firefox(service=geckodriver_service, options=options)
    driver.implicitly_wait(10)

    yield driver

    # Collect console logs if any (best effort)
    try:
        logs = driver.get_log("browser")
        if logs:
            print("\n--- Browser Console Logs ---")
            for log in logs:
                print(f"[{log['level']}] {log['message']}")
            print("--- End Logs ---\n")
    except Exception:
        pass

    driver.quit()


# --- URL Fixtures ---

@pytest.fixture(scope="session")
def base_url() -> str:
    return FRONTEND_URL


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return API_BASE_URL


# --- Auth Fixtures ---

@pytest.fixture(scope="session")
def test_credentials():
    """Generate test user credentials (created once per session)."""
    label = _generate_test_label()
    return {
        "email": f"{label}@aerialcast.test",
        "password": "TestPass123!",
        "full_name": f"Test User {label}",
    }


@pytest.fixture(scope="session")
def test_admin_token(api_base_url, test_credentials):
    """Register a test user and obtain JWT token via API."""
    # Step 1: Register (200 = success, 409 = already exists)
    register_resp = requests.post(
        f"{api_base_url}/auth/register",
        json=test_credentials,
        timeout=30,
    )
    if register_resp.status_code in (200, 201):
        print(f"User registered: {test_credentials['email']}")
    elif register_resp.status_code == 409:
        print("User already exists, proceeding to login...")
    else:
        pytest.fail(f"Failed to register test user: {register_resp.status_code} - {register_resp.text}")

    # Step 2: Login
    login_resp = requests.post(
        f"{api_base_url}/auth/login",
        json={
            "email": test_credentials["email"],
            "password": test_credentials["password"],
        },
        timeout=30,
    )
    if login_resp.status_code != 200:
        pytest.fail(f"Failed to login test user: {login_resp.text}")

    data = login_resp.json()
    token = data.get("access_token")
    user = data.get("user", {})

    if not token:
        pytest.fail("No access_token in login response")

    return {
        "token": token,
        "user": user,
        "email": test_credentials["email"],
        "password": test_credentials["password"],
    }


@pytest.fixture(scope="function")
def authenticated_driver(driver, base_url, test_admin_token):
    """Provide a driver that is already logged in."""
    # Inject token into localStorage
    driver.get(base_url)
    time.sleep(1)  # Wait for page load
    driver.execute_script(
        f"localStorage.setItem('token', '{test_admin_token['token']}');"
    )
    driver.execute_script(
        f"localStorage.setItem('user', '{json.dumps(test_admin_token['user'])}');"
    )
    # Refresh to pick up auth state
    driver.refresh()
    time.sleep(2)
    yield driver


# --- DB Helper Fixture ---

@pytest.fixture(scope="session")
def db_helper():
    """Provide DB helper for cleanup and verification."""
    helper = DBHelper()
    yield helper


# --- Cleanup Fixture ---

@pytest.fixture(scope="function", autouse=True)
def cleanup_test_data(request, db_helper):
    """Automatically cleanup TEST-* data after each test."""
    yield
    # Cleanup after test
    try:
        db_helper.cleanup_test_data()
        print("\n[INFO] Cleanup TEST data completed.")
    except Exception as e:
        print(f"\n[WARN] Cleanup failed: {e}")


# --- Mock Drone Fixture ---

@pytest.fixture(scope="function")
def mock_drone():
    """Provide a mock drone publisher that can be started/stopped."""
    publisher = MockDronePublisher()
    yield publisher
    publisher.stop()


# --- Test Data Label Fixture ---

@pytest.fixture(scope="function")
def test_label() -> str:
    """Generate a unique label for this test function."""
    return _generate_test_label()
