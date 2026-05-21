import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Inisialisasi WebDriver
driver = webdriver.Chrome()

# Membuka halaman web Google
driver.get("https://www.google.com")

# Mencari elemen input pencarian menggunakan ID
search_input = driver.find_element(By.NAME, "q")

# Memasukkan kata kunci pencarian
search_input.send_keys("kampus digital masa gitu")

# Menekan tombol Enter untuk melakukan pencarian
search_input.send_keys(Keys.ENTER)

# Tambahkan penundaan waktu untuk melihat hasil pencarian
time.sleep(10)

# Tidak menutup WebDriver

# Anda dapat melanjutkan dengan mengambil tindakan lain pada halaman yang terbuka

# Misalnya, dapatkan judul halaman saat ini
page_title = driver.title
print("Judul halaman:", page_title)

# Menutup WebDriver
driver.quit()
