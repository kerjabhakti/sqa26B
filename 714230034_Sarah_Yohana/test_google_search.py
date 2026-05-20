import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()

driver.get("https://www.google.com")

search_input = driver.find_element(By.NAME, "q")

search_input.send_keys("kampus digital masa gitu")

search_input.send_keys(Keys.ENTER)

time.sleep(10)

page_title = driver.title
print("Judul halaman:", page_title)

driver.quit()