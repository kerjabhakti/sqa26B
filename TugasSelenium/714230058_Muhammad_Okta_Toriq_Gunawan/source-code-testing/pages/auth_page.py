"""Auth Page Object - Login / Register flows."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class AuthPage(BasePage):
    """Page Object for /auth (login & register)."""

    PATH = "/auth"

    # Selectors (based on actual auth form implementation)
    LOGIN_TAB = (By.XPATH, "//button[@role='tab' and contains(., 'Login')]")
    REGISTER_TAB = (By.XPATH, "//button[@role='tab' and contains(., 'Register')]")
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    FULL_NAME_INPUT = (By.ID, "fullName")
    CONFIRM_PASSWORD_INPUT = (By.ID, "confirmPassword")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit' and contains(., 'Login')]")
    REGISTER_BUTTON = (By.XPATH, "//button[@type='submit' and contains(., 'Create Account')]")
    ERROR_ALERT = (By.XPATH, "//div[@role='alert']")
    TOAST_MESSAGE = (By.XPATH, "//div[contains(@class, 'toast') or contains(@class, 'Toast')]")

    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        super().open(self.PATH)

    def login(self, email: str, password: str):
        """Login via UI form."""
        self.open()
        time.sleep(2)

        # Ensure we're on login tab
        self.click(*self.LOGIN_TAB)
        time.sleep(1)

        self.send_keys(*self.EMAIL_INPUT, email)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.click(*self.LOGIN_BUTTON)

        # Wait for redirect or toast
        time.sleep(3)

    def register(self, full_name: str, email: str, password: str):
        """Register a new user via UI form."""
        self.open()
        time.sleep(2)

        # Switch to register tab
        self.click(*self.REGISTER_TAB)
        time.sleep(1)

        self.send_keys(*self.FULL_NAME_INPUT, full_name)
        self.send_keys(*self.EMAIL_INPUT, email)
        self.send_keys(*self.PASSWORD_INPUT, password)
        self.send_keys(*self.CONFIRM_PASSWORD_INPUT, password)

        self.click(*self.REGISTER_BUTTON)
        time.sleep(3)

    def is_logged_in(self) -> bool:
        """Check if currently on dashboard (redirected after login)."""
        return "/auth" not in self.driver.current_url

    def get_error_message(self) -> str:
        """Extract error message from alert or toast."""
        try:
            el = self.find(*self.ERROR_ALERT, timeout=3)
            return el.text.strip()
        except Exception:
            return ""

    def logout(self):
        """Clear localStorage and redirect to auth."""
        self.driver.execute_script("localStorage.clear();")
        self.open()
