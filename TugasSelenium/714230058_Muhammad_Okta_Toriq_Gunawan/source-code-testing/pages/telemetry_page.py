"""Telemetry Page Object - Live telemetry and replay views."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class TelemetryPage(BasePage):
    """Page Object for live telemetry monitoring and replay."""

    # Map and telemetry components
    MAP_CONTAINER = (By.XPATH, "//div[contains(@class,'leaflet-container')] | //div[contains(@class,'Map')] | //*[contains(@class,'map')]")
    VITALS_CARD = (By.XPATH, "//div[contains(.,'Battery') or contains(.,'Altitude') or contains(@class,'vitals')]")
    EVENT_FEED = (By.XPATH, "//div[contains(@class,'feed') or contains(.,'Events')] | //div[contains(@class,'EventFeed')]")
    STATUS_INDICATOR = (By.XPATH, "//div[contains(@class,'status') or contains(@class,'Status')] | //span[contains(@class,'badge')]")

    # Vitals specific
    BATTERY_VALUE = (By.XPATH, "//*[contains(text(),'Battery')]/following-sibling::*[1] | //*[contains(text(),'Battery')]/ancestor::*[1]//*[contains(@class,'value')]")
    ALTITUDE_VALUE = (By.XPATH, "//*[contains(text(),'Altitude')]/following-sibling::*[1] | //*[contains(text(),'Altitude')]/ancestor::*[1]//*[contains(@class,'value')]")
    SPEED_VALUE = (By.XPATH, "//*[contains(text(),'Speed')]/following-sibling::*[1] | //*[contains(text(),'Speed')]/ancestor::*[1]//*[contains(@class,'value')]")
    SIGNAL_VALUE = (By.XPATH, "//*[contains(text(),'Signal') or contains(text(),'RSSI')]/following-sibling::*[1]")
    SNR_VALUE = (By.XPATH, "//*[contains(text(),'SNR')]/following-sibling::*[1]")

    # Replay controls
    PLAY_BUTTON = (By.XPATH, "//button[contains(@aria-label,'play') or contains(text(),'Play')]")
    PAUSE_BUTTON = (By.XPATH, "//button[contains(@aria-label,'pause') or contains(text(),'Pause')]")
    TIMELINE = (By.XPATH, "//div[contains(@class,'timeline') or contains(@class,'slider')]")
    SPEED_SELECT = (By.XPATH, "//select | //button[@role='combobox']")

    # Session selector
    SESSION_SELECTOR = (By.XPATH, "//select | //div[contains(@class,'SessionSelector')]")

    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)

    # --- Assertions for telemetry display ---

    def assert_map_rendered(self) -> bool:
        """Check if Leaflet map is visible."""
        return self.is_visible(*self.MAP_CONTAINER)

    def assert_vitals_visible(self) -> bool:
        """Check if vitals panel is visible."""
        return self.is_visible(*self.VITALS_CARD)

    def assert_event_feed_visible(self) -> bool:
        """Check if event feed is visible."""
        return self.is_visible(*self.EVENT_FEED)

    def get_battery_text(self) -> str:
        try:
            return self.get_text(*self.BATTERY_VALUE)
        except Exception:
            return ""

    def get_altitude_text(self) -> str:
        try:
            return self.get_text(*self.ALTITUDE_VALUE)
        except Exception:
            return ""

    def get_speed_text(self) -> str:
        try:
            return self.get_text(*self.SPEED_VALUE)
        except Exception:
            return ""

    def get_signal_text(self) -> str:
        try:
            return self.get_text(*self.SIGNAL_VALUE)
        except Exception:
            return ""

    def get_snr_text(self) -> str:
        try:
            return self.get_text(*self.SNR_VALUE)
        except Exception:
            return ""

    def get_status_text(self) -> str:
        try:
            return self.get_text(*self.STATUS_INDICATOR)
        except Exception:
            return ""

    def get_event_count(self) -> int:
        """Count event items in feed."""
        try:
            events = self.find_all(By.XPATH, "//div[contains(@class,'feed')]//div[contains(@class,'item')] | //div[contains(@class,'event')]", timeout=5)
            return len(events)
        except Exception:
            return 0

    def wait_for_telemetry_update(self, previous_battery: str, timeout: int = 12) -> bool:
        """Wait for battery value to change (indicating polling update)."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.get_battery_text() != previous_battery
            )
            return True
        except Exception:
            return False

    def assert_no_console_severe_errors(self) -> bool:
        """Assert no SEVERE console errors."""
        return not self.has_console_errors()

    def screenshot_telemetry(self, name: str = "telemetry"):
        self.screenshot(name)
