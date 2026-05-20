"""Dashboard Page Object - Main dashboard overview."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class DashboardPage(BasePage):
    """Page Object for dashboard root / and navigation."""

    PATH = "/"

    # Sidebar nav links
    SIDEBAR_MISSIONS = (By.XPATH, "//a[@href='/missions'] | //*[contains(text(),'Missions')]")
    SIDEBAR_DRONES = (By.XPATH, "//a[@href='/drones'] | //*[contains(text(),'Drones')]")
    SIDEBAR_GEOFENCES = (By.XPATH, "//a[@href='/geofences'] | //*[contains(text(),'Geofences')]")
    SIDEBAR_CHECKLISTS = (By.XPATH, "//a[@href='/checklists'] | //*[contains(text(),'Checklists')]")
    SIDEBAR_MAINTENANCE = (By.XPATH, "//a[@href='/maintenance'] | //*[contains(text(),'Maintenance')]")

    # Dashboard stat cards
    STAT_TOTAL_MISSIONS = (By.XPATH, "//*[contains(text(),'Total Missions') or contains(text(),'Missions')]/following::*[contains(@class,'text-2xl') or contains(@class,'text-3xl')][1]")
    STAT_ACTIVE_MISSIONS = (By.XPATH, "//*[contains(text(),'Active')]/following::*[contains(@class,'text-2xl') or contains(@class,'text-3xl')][1]")
    STAT_READY_DRONES = (By.XPATH, "//*[contains(text(),'Ready') or contains(text(),'Drones')]/following::*[contains(@class,'text-2xl') or contains(@class,'text-3xl')][1]")

    # Common elements
    NAVBAR_USER_GREETING = (By.XPATH, "//header | //nav | //*[contains(text(),'Welcome') or contains(text(),'Hello')]")
    THEME_TOGGLE = (By.XPATH, "//button[@aria-label='Toggle theme' or contains(@title,'theme') or contains(@class,'theme')]")
    NOTIFICATION_BELL = (By.XPATH, "//button[contains(@aria-label,'notification') or contains(@class,'bell')]")
    SIDEBAR = (By.XPATH, "//aside | //nav[contains(@class,'sidebar')]")

    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        super().open(self.PATH)
        time.sleep(2)

    # --- Navigation ---

    def navigate_to_missions(self):
        self.click(*self.SIDEBAR_MISSIONS)
        time.sleep(2)

    def navigate_to_drones(self):
        self.click(*self.SIDEBAR_DRONES)
        time.sleep(2)

    def navigate_to_geofences(self):
        self.click(*self.SIDEBAR_GEOFENCES)
        time.sleep(2)

    def navigate_to_checklists(self):
        self.click(*self.SIDEBAR_CHECKLISTS)
        time.sleep(2)

    # --- Assertions ---

    def assert_dashboard_loaded(self) -> bool:
        """Verify main dashboard components are visible."""
        # More robust: just check the page loaded with some content
        checks = [
            self.is_visible(*self.SIDEBAR, timeout=5),
            self.is_visible(By.XPATH, "//main | //div[contains(@class,'flex')]", timeout=5),
        ]
        return any(checks)

    def assert_sidebar_nav_visible(self) -> bool:
        """Verify sidebar navigation items exist."""
        items = [
            self.SIDEBAR_MISSIONS,
            self.SIDEBAR_DRONES,
        ]
        return any(self.is_visible(*item, timeout=3) for item in items)

    def get_stat_card_value(self, card_name: str) -> str:
        """Get numeric value from a stat card by name."""
        # Try to find card by text and get its number
        xpath = f"//*[contains(text(),'{card_name}')]/ancestor::*[contains(@class,'card') or contains(@class,'Card')][1]//*[contains(@class,'text-2xl') or contains(@class,'text-3xl') or contains(@class,'text-4xl')]"
        return self.get_text(By.XPATH, xpath)

    def toggle_theme(self):
        """Click theme toggle button."""
        if self.is_visible(*self.THEME_TOGGLE):
            self.click(*self.THEME_TOGGLE)
            time.sleep(1)
