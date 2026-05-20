from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inisialisasi WebDriver untuk Chrome
driver = webdriver.Chrome()

try:
    # Membuka halaman web Google
    driver.get("https://www.google.com")

    # Mencari elemen input pencarian dan memasukkan kata kunci
    search_input = driver.find_element(By.NAME, "q")
    search_input.send_keys("kampus digital masa gitu")
    search_input.send_keys(Keys.ENTER)

    # Menunggu hingga judul halaman hasil pencarian muncul dan mengandung kata kunci
    WebDriverWait(driver, 10).until(
        EC.title_contains("kampus digital masa gitu")
    )

    # Mendapatkan dan menampilkan judul halaman
    page_title = driver.title
    print(f"Judul halaman hasil pencarian: {page_title}")

finally:
    # Menutup browser
    driver.quit()
