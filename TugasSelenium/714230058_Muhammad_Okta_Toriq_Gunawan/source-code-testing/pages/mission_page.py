"""Mission Page Object - Mission planning CRUD."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class MissionPage(BasePage):
    """Page Object for /missions and mission creation."""

    PATH = "/missions"

    CREATE_BUTTON = (By.XPATH, "//button[contains(text(),'Add mission') or contains(text(),'Add Mission')]")
    MISSION_CARD = (By.XPATH, "//div[contains(@class,'card') and .//h3] | //article | //div[contains(@class,'MissionCard')]")

    # Create dialog
    DIALOG = (By.XPATH, "//div[@role='dialog']")
    MISSION_NAME_INPUT = (By.XPATH, "//div[@role='dialog']//input[@placeholder='Mission Name' or @name='mission_name']")
    NOTES_INPUT = (By.XPATH, "//div[@role='dialog']//textarea[@placeholder='Notes' or @name='notes']")
    DRONE_SELECT = (By.XPATH, "//div[@role='dialog']//select[@name='drone_id'] | //div[@role='dialog']//button[@role='combobox']")
    SAVE_AS_DRAFT_CHECKBOX = (By.XPATH, "//div[@role='dialog']//input[@type='checkbox' and @name='save_as_draft']")
    ADD_WAYPOINT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[contains(text(),'Add Waypoint') or contains(text(),'Waypoint')]")
    SUBMIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[@type='submit' or contains(text(),'Save') or contains(text(),'Create')]")

    # Waypoint fields (dynamic - last added)
    WP_LAT_INPUT = (By.XPATH, "(//div[@role='dialog']//input[@placeholder='Latitude' or @name='latitude'])[last()]")
    WP_LON_INPUT = (By.XPATH, "(//div[@role='dialog']//input[@placeholder='Longitude' or @name='longitude'])[last()]")
    WP_ORDER_INPUT = (By.XPATH, "(//div[@role='dialog']//input[@placeholder='Order' or @name='order'])[last()]")

    # Mission detail
    STATUS_BADGE = (By.XPATH, "//span[contains(@class,'badge') or contains(@class,'Badge')] | //div[contains(text(),'DRAFT') or contains(text(),'PENDING')]")
    SUBMIT_BUTTON_STATUS = (By.XPATH, "//button[contains(text(),'Submit')]")
    APPROVE_BUTTON = (By.XPATH, "//button[contains(text(),'Approve')]")

    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        super().open(self.PATH)
        time.sleep(2)

    def create_mission(self, name: str, notes: str, drone_id: str | None = None, waypoints: list | None = None, save_as_draft: bool = True) -> bool:
        """Create a mission with waypoints via UI."""
        self.open()
        time.sleep(1)

        self.click(*self.CREATE_BUTTON)
        time.sleep(1)

        # Fill basic info
        self.send_keys(*self.MISSION_NAME_INPUT, name)
        self.send_keys(*self.NOTES_INPUT, notes)

        # Select drone if dropdown exists
        if drone_id:
            try:
                self.click(*self.DRONE_SELECT)
                time.sleep(0.5)
                # Click option with drone_id
                option_xpath = f"//div[@role='dialog']//li[contains(.,'{drone_id}')] | //option[contains(.,'{drone_id}')]"
                self.click(By.XPATH, option_xpath)
                time.sleep(0.5)
            except Exception:
                pass

        # Add waypoints
        if waypoints:
            for wp in waypoints:
                self.click(*self.ADD_WAYPOINT_BUTTON)
                time.sleep(0.5)
                self.send_keys(*self.WP_LAT_INPUT, str(wp["lat"]))
                self.send_keys(*self.WP_LON_INPUT, str(wp["lon"]))
                self.send_keys(*self.WP_ORDER_INPUT, str(wp.get("order", 1)))
                time.sleep(0.3)

        # Submit
        self.click(*self.SUBMIT_BUTTON)
        time.sleep(3)

        return self.is_mission_present(name)

    def is_mission_present(self, name: str) -> bool:
        """Check if mission card exists."""
        xpath = f"//*[contains(text(), \"{name}\")]"
        return self.is_visible(By.XPATH, xpath, timeout=5)

    def get_mission_status(self) -> str:
        """Get status text from badge."""
        try:
            return self.get_text(*self.STATUS_BADGE, timeout=3)
        except Exception:
            return ""

    def open_mission_detail(self, mission_name: str):
        """Click on mission card to open detail."""
        xpath = f"//div[contains(., '{mission_name}')]"
        self.click(By.XPATH, xpath)
        time.sleep(2)
