import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture to initialize and teardown the Selenium Chrome WebDriver.
    By default, it runs in headless mode to work seamlessly on background environments.
    You can disable headless mode by setting the environment variable SELENIUM_HEADLESS=false.
    """
    headless_env = os.getenv("SELENIUM_HEADLESS", "true").lower()
    headless = headless_env in ("true", "1", "yes")
    
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Initialize webdriver. Selenium Manager will automatically download/cache
    # Chrome for Testing and chromedriver if they are not installed.
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    # Cleanup browser process
    driver.quit()
