"""Base Page Object with common Selenium utilities."""

from __future__ import annotations

import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
)


class BasePage:
    """Base class for all Page Objects."""

    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")
        self.wait = WebDriverWait(driver, 15)
        self.short_wait = WebDriverWait(driver, 5)

    # --- Navigation ---

    def open(self, path: str = ""):
        """Open a page by path."""
        url = f"{self.base_url}{path}"
        self.driver.get(url)
        time.sleep(1)

    def refresh(self):
        self.driver.refresh()
        time.sleep(1)

    # --- Element Helpers ---

    def find(self, by: By, value: str, timeout: int = 10) -> WebElement:
        """Find element with explicit wait."""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def find_all(self, by: By, value: str, timeout: int = 10) -> list[WebElement]:
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((by, value)))

    def click(self, by: By, value: str, timeout: int = 10):
        """Wait for clickable then click."""
        wait = WebDriverWait(self.driver, timeout)
        el = wait.until(EC.element_to_be_clickable((by, value)))
        el.click()
        time.sleep(0.5)

    def send_keys(self, by: By, value: str, text: str, timeout: int = 10):
        """Find input and type text."""
        el = self.find(by, value, timeout)
        el.clear()
        el.send_keys(text)
        time.sleep(0.3)

    def get_text(self, by: By, value: str, timeout: int = 10) -> str:
        el = self.find(by, value, timeout)
        return el.text.strip()

    def is_visible(self, by: By, value: str, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    def is_present(self, by: By, value: str, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False

    # --- Text-based finders (robust when no stable IDs) ---

    def find_by_text(self, text: str, tag: str = "*", timeout: int = 10) -> WebElement:
        xpath = f"//{tag}[contains(text(), '{text}')]"
        return self.find(By.XPATH, xpath, timeout)

    def click_by_text(self, text: str, tag: str = "*", timeout: int = 10):
        xpath = f"//{tag}[contains(text(), '{text}')]"
        self.click(By.XPATH, xpath, timeout)

    def find_by_aria_label(self, label: str, timeout: int = 10) -> WebElement:
        return self.find(By.CSS_SELECTOR, f"[aria-label='{label}']", timeout)

    def find_by_placeholder(self, placeholder: str, timeout: int = 10) -> WebElement:
        return self.find(By.CSS_SELECTOR, f"[placeholder='{placeholder}']", timeout)

    # --- Wait conditions ---

    def wait_for_text(self, by: By, value: str, text: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element((by, value), text)
        )

    def wait_for_url_contains(self, fragment: str, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(fragment)
        )

    def wait_for_stale(self, element: WebElement, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(EC.staleness_of(element))

    def wait_for_invisible(self, by: By, value: str, timeout: int = 10):
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((by, value))
        )

    # --- Screenshot ---

    def screenshot(self, name: str):
        """Save screenshot to /tmp."""
        path = f"/tmp/selenium_{name}_{int(time.time())}.png"
        self.driver.save_screenshot(path)
        print(f"[Screenshot] Saved to {path}")

    # --- Console error check ---

    def has_console_errors(self) -> bool:
        """Return True if there are SEVERE console logs."""
        try:
            logs = self.driver.get_log("browser")
            severe = [l for l in logs if l.get("level") == "SEVERE"]
            if severe:
                print(f"[Console Error] {len(severe)} SEVERE logs found")
                for log in severe[:5]:
                    print(f"  - {log['message']}")
            return len(severe) > 0
        except Exception:
            return False

    # --- Scroll ---

    def scroll_to_element(self, element: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(0.5)

    def scroll_down(self, pixels: int = 500):
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")
        time.sleep(0.3)
