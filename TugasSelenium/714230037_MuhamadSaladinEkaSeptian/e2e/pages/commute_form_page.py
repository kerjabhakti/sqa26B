from selenium.webdriver.common.by import By

from e2e.utils.waits import wait_clickable, wait_visible
from e2e.utils.selectors import by_testid


class CommuteFormPage:
    def __init__(self, driver):
        self.driver = driver

    def wait_loaded(self):
        wait_visible(self.driver, *by_testid("form-title"))

    def set_name(self, name):
        field = wait_visible(self.driver, *by_testid("commute-name"))
        field.clear()
        field.send_keys(name)

    def pick_home(self):
        wait_clickable(self.driver, *by_testid("pick-home")).click()

    def pick_office(self):
        wait_clickable(self.driver, *by_testid("pick-office")).click()

    def select_vehicle(self, vehicle_value):
        select = wait_visible(self.driver, *by_testid("vehicle-select"))
        select.click()
        select.send_keys(vehicle_value)

    def set_fuel_price(self, price):
        field = wait_visible(self.driver, *by_testid("fuel-price"))
        field.clear()
        field.send_keys(str(price))

    def set_days_per_week(self, days):
        wait_clickable(self.driver, *by_testid(f"days-per-week-{days}")).click()

    def submit(self):
        wait_clickable(self.driver, *by_testid("submit-commute")).click()

    def back(self):
        wait_clickable(self.driver, *by_testid("form-back")).click()

    def map_click(self, x_offset=100, y_offset=100):
        map_el = wait_visible(self.driver, By.CSS_SELECTOR, "[data-testid='map']")
        self.driver.execute_script(
            "const rect = arguments[0].getBoundingClientRect();"
            "const x = rect.left + arguments[1];"
            "const y = rect.top + arguments[2];"
            "const target = document.elementFromPoint(x, y);"
            "if (target) { target.dispatchEvent(new MouseEvent('click', {clientX: x, clientY: y, bubbles: true})); }",
            map_el,
            x_offset,
            y_offset,
        )
