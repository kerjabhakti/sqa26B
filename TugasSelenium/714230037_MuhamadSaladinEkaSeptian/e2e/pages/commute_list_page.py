from selenium.webdriver.common.by import By

from e2e.utils.waits import wait_clickable, wait_visible
from e2e.utils.selectors import by_testid


class CommuteListPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_list(self):
        wait_visible(self.driver, *by_testid("commute-list"))

    def commute_cards(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "[data-testid^='commute-card-']")

    def first_commute_id(self):
        cards = self.commute_cards()
        if not cards:
            return None
        return cards[0].get_attribute("data-testid").replace("commute-card-", "")

    def open_commute(self, commute_id):
        wait_clickable(self.driver, By.CSS_SELECTOR, f"[data-testid='commute-card-{commute_id}']").click()

    def open_edit(self, commute_id):
        wait_clickable(self.driver, By.CSS_SELECTOR, f"[data-testid='edit-commute-{commute_id}']").click()

    def delete(self, commute_id):
        wait_clickable(self.driver, By.CSS_SELECTOR, f"[data-testid='delete-commute-{commute_id}']").click()

    def read_commute_name(self, commute_id):
        return wait_visible(self.driver, By.CSS_SELECTOR, f"[data-testid='commute-name-{commute_id}']").text

    def read_annual_cost(self, commute_id):
        return wait_visible(self.driver, By.CSS_SELECTOR, f"[data-testid='commute-annual-cost-{commute_id}']").text

    def read_annual_workdays(self, commute_id):
        return wait_visible(self.driver, By.CSS_SELECTOR, f"[data-testid='commute-annual-workdays-{commute_id}']").text
