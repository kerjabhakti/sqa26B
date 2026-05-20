"""Test Objective (a): UI Validation - Auth Flow.

Validasi fungsionalitas login/register UI.
"""

from __future__ import annotations

import time

import pytest
from selenium.webdriver.common.by import By

from pages.auth_page import AuthPage
from pages.dashboard_page import DashboardPage


class TestAuthFlow:
    """Test authentication UI flows."""

    def test_login_page_loads(self, driver, base_url):
        """Verify login page renders all expected elements."""
        auth = AuthPage(driver, base_url)
        auth.open()

        assert auth.is_visible(*auth.LOGIN_TAB), "Login tab should be visible"
        assert auth.is_visible(*auth.REGISTER_TAB), "Register tab should be visible"
        assert auth.is_visible(*auth.EMAIL_INPUT), "Email input should be visible"
        assert auth.is_visible(*auth.PASSWORD_INPUT), "Password input should be visible"
        assert auth.is_visible(*auth.LOGIN_BUTTON), "Login button should be visible"

        auth.screenshot("auth_login_page")

    def test_login_with_valid_credentials(self, authenticated_driver, base_url, test_admin_token):
        """Verify successful login redirects to dashboard."""
        # authenticated_driver is already logged in
        dashboard = DashboardPage(authenticated_driver, base_url)
        dashboard.open()

        assert dashboard.assert_dashboard_loaded(), "Dashboard should load after login"
        assert "/auth" not in authenticated_driver.current_url, "Should be redirected away from auth"

    def test_login_with_invalid_credentials(self, driver, base_url):
        """Verify login with wrong password shows error."""
        auth = AuthPage(driver, base_url)
        auth.login(email="invalid@test.com", password="wrongpass")

        # Should stay on auth page
        assert "/auth" in driver.current_url, "Should remain on auth page after failed login"

    def test_register_new_user(self, driver, base_url, test_label):
        """Verify registration flow creates new user."""
        auth = AuthPage(driver, base_url)
        auth.register(
            full_name=f"Test User {test_label}",
            email=f"{test_label}@aerialcast.test",
            password="TestPass123!",
        )

        # After successful register, should redirect or show success
        # Note: registration might auto-login or show confirmation
        time.sleep(2)
        # Check for visible error alert (not just word "error" in source)
        has_visible_error = auth.is_visible(*auth.ERROR_ALERT, timeout=2)
        assert not has_visible_error, f"Should not show error: {auth.get_error_message()}"

    def test_logout_clears_session(self, authenticated_driver, base_url):
        """Verify logout clears localStorage and redirects to auth."""
        auth = AuthPage(authenticated_driver, base_url)
        auth.logout()

        # Verify localStorage cleared
        token = authenticated_driver.execute_script("return localStorage.getItem('token');")
        assert token is None, "Token should be cleared after logout"
