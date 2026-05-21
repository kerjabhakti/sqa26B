import os
from datetime import datetime

import pytest
import requests
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default="https://commute.irc-enter.tech")
    parser.addoption("--api-url", action="store", default="https://commute.irc-enter.tech/api/v1")
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url")


@pytest.fixture(scope="session")
def api_url(request):
    return request.config.getoption("--api-url")


@pytest.fixture(scope="session")
def driver(request):
    headless = request.config.getoption("--headless")
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,900")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def set_device_id(driver, base_url):
    device_id = os.environ.get("E2E_DEVICE_ID", "e2e-device-id")
    driver.get(base_url)
    driver.execute_script(
        "window.localStorage.setItem('device_id', arguments[0]);",
        device_id,
    )
    yield device_id


@pytest.fixture(autouse=True)
def clear_commutes(api_url):
    device_id = os.environ.get("E2E_DEVICE_ID", "e2e-device-id")
    try:
        response = requests.get(f"{api_url}/commutes", params={"device_id": device_id}, timeout=10)
        response.raise_for_status()
        payload = response.json()
        commutes = payload.get("data", {}).get("commutes", [])
        for commute in commutes:
            requests.delete(f"{api_url}/commutes/{commute['id']}", timeout=10)
    except requests.RequestException:
        pass
    yield


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or report.passed:
        return
    driver = item.funcargs.get("driver")
    if not driver:
        return
    artifacts_dir = os.path.join("artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    name = report.nodeid.replace("/", "_").replace(":", "_")

    try:
        screenshot_path = os.path.join(artifacts_dir, f"{name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
    except WebDriverException:
        pass

    try:
        html_path = os.path.join(artifacts_dir, f"{name}_{timestamp}.html")
        with open(html_path, "w", encoding="utf-8") as html_file:
            html_file.write(driver.page_source)
    except OSError:
        pass
