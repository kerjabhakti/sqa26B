from selenium.webdriver.common.by import By


def by_testid(value):
    return (By.CSS_SELECTOR, f"[data-testid='{value}']")
