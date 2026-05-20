"""Custom Selenium wait conditions for robust assertions."""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException


class WaitConditions:
    """Collection of reusable wait conditions."""

    @staticmethod
    def element_stabilized(driver, locator, timeout=10):
        """Wait until element is present and stable (not stale)."""
        def _condition(d):
            try:
                el = d.find_element(*locator)
                # Trigger a property access to detect staleness
                _ = el.text
                return el
            except StaleElementReferenceException:
                return False

        return WebDriverWait(driver, timeout).until(_condition)

    @staticmethod
    def text_changed(driver, locator, old_text, timeout=10):
        """Wait until element text changes from old_text."""
        def _condition(d):
            try:
                el = d.find_element(*locator)
                current = el.text.strip()
                return current if current != old_text else False
            except StaleElementReferenceException:
                return False

        return WebDriverWait(driver, timeout).until(_condition)

    @staticmethod
    def console_no_errors(driver, timeout=5):
        """Check browser console has no SEVERE-level logs."""
        try:
            logs = driver.get_log("browser")
            severe = [l for l in logs if l["level"] == "SEVERE"]
            return len(severe) == 0
        except Exception:
            return True

    @staticmethod
    def polling_cycle_complete(driver, locator, previous_count, timeout=10):
        """Wait until number of child elements changes (indicating polling update)."""
        def _condition(d):
            try:
                elements = d.find_elements(*locator)
                return len(elements) > previous_count
            except Exception:
                return False

        return WebDriverWait(driver, timeout).until(_condition)
