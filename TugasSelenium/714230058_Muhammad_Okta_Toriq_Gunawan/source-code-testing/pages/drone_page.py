"""Drone Page Object - Fleet CRUD operations."""

from __future__ import annotations

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from .base_page import BasePage


class DronePage(BasePage):
    """Page Object for /drones (fleet management)."""

    PATH = "/drones"

    CREATE_BUTTON = (By.XPATH, "//button[contains(text(),'Add Drone') or contains(text(),'Create') or contains(@aria-label,'add')]")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search' or contains(@aria-label,'search')]")

    # Dialog form
    DIALOG = (By.XPATH, "//div[@role='dialog'] | //div[contains(@class,'Dialog')]")
    NAME_INPUT = (By.XPATH, "//div[@role='dialog']//input[@placeholder='Name' or @name='name']")
    MODEL_INPUT = (By.XPATH, "//div[@role='dialog']//input[@placeholder='Model' or @name='model']")
    LORA_ID_INPUT = (By.XPATH, "//div[@role='dialog']//input[@placeholder='LoRa ID' or @name='lora_id']")
    SUBMIT_BUTTON = (By.XPATH, "//div[@role='dialog']//button[@type='submit' or contains(text(),'Save') or contains(text(),'Create')]")
    CANCEL_BUTTON = (By.XPATH, "//div[@role='dialog']//button[contains(text(),'Cancel')]")

    # Drone cards
    DRONE_CARD = (By.XPATH, "//div[contains(@class,'card')] | //article | //div[contains(@class,'rounded-lg')]")
    DRONE_NAME = (By.XPATH, ".//h3 | .//*[contains(@class,'title')]")
    DRONE_STATUS = (By.XPATH, ".//span[contains(@class,'badge') or contains(@class,'status')]")
    EDIT_BUTTON = (By.XPATH, ".//button[contains(@aria-label,'edit') or contains(text(),'Edit')]")
    DELETE_BUTTON = (By.XPATH, ".//button[contains(@aria-label,'delete') or contains(text(),'Delete')]")

    def __init__(self, driver: WebDriver, base_url: str):
        super().__init__(driver, base_url)

    def open(self):
        super().open(self.PATH)
        time.sleep(2)

    def create_drone(self, name: str, model: str, lora_id: str) -> bool:
        """Create a new drone via UI dialog."""
        self.open()
        time.sleep(1)

        self.click(*self.CREATE_BUTTON)
        time.sleep(1)

        self.send_keys(*self.NAME_INPUT, name)
        self.send_keys(*self.MODEL_INPUT, model)
        self.send_keys(*self.LORA_ID_INPUT, lora_id)

        self.click(*self.SUBMIT_BUTTON)
        time.sleep(3)

        # Verify card appears
        return self.is_drone_present(lora_id)

    def is_drone_present(self, lora_id: str) -> bool:
        """Check if a drone card with given lora_id exists."""
        xpath = f"//div[contains(., '{lora_id}')]"
        return self.is_visible(By.XPATH, xpath, timeout=5)

    def get_drone_count(self) -> int:
        """Count drone cards on page."""
        try:
            cards = self.find_all(*self.DRONE_CARD, timeout=5)
            return len(cards)
        except Exception:
            return 0

    def delete_drone(self, lora_id: str) -> bool:
        """Find and delete drone by lora_id."""
        try:
            card_xpath = f"//div[contains(., '{lora_id}')]"
            card = self.find(By.XPATH, card_xpath)
            # Find delete button within card
            delete_btn = card.find_element(By.XPATH, ".//button[contains(@aria-label,'delete') or contains(text(),'Delete')]")
            delete_btn.click()
            time.sleep(2)
            # Confirm delete if dialog appears
            confirm = self.is_visible(By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Yes')]", timeout=3)
            if confirm:
                self.click(By.XPATH, "//button[contains(text(),'Confirm') or contains(text(),'Yes')]")
                time.sleep(2)
            return True
        except Exception:
            return False
