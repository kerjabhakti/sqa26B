import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

print("Menginisialisasi Chrome WebDriver...")
driver = webdriver.Chrome()

print("Membuka halaman Google...")
driver.get("https://www.google.com")

print("Mencari kolom pencarian...")
search_input = driver.find_element(By.NAME, "q")

keyword = "kampus digital masa gitu"

print(f"Memasukkan kata kunci pencarian: '{keyword}'")
search_input.send_keys(keyword)

search_input.send_keys(Keys.ENTER)

print("Menunggu 5 detik untuk memuat hasil pencarian...")
time.sleep(5)

print("\n=== Hasil Pengujian ===")

current_url = driver.current_url
print("URL halaman:", current_url)

assert "search" in current_url

print("Pengujian Berhasil! Halaman pencarian telah dimuat.")
print("========================")

print("\nMenutup WebDriver...")
driver.quit()