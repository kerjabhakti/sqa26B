from selenium.webdriver.common.by import By

from e2e.utils.waits import wait_clickable, wait_visible
from e2e.utils.selectors import by_testid


class AppPage:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url

    def open(self):
        self.driver.get(self.base_url)
        wait_visible(self.driver, *by_testid("app-title"))

    def click_add_commute(self):
        wait_clickable(self.driver, *by_testid("add-commute")).click()

    def open_first_commute(self):
        wait_clickable(self.driver, *by_testid("commute-list"))
        cards = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='commute-card-']")
        if cards:
            cards[0].click()

    def wait_empty_state(self):
        wait_visible(self.driver, *by_testid("empty-state"))
