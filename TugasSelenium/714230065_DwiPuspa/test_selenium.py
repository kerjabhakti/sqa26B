import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

#Maksimalkan ukuran jendela browser agar kolom pencarian tidak tersembunyi!
browser.maximize_window() 

# Mengakses halaman utama Wikipedia Bahasa Indonesia
browser.get("https://id.wikipedia.org/")

# menggunakan CSS_SELECTOR agar Selenium langsung menemukan kolom yang terlihat
kolom_pencarian = browser.find_element(By.CSS_SELECTOR, "input[type='search']")

kata_kunci = "Pengujian perangkat lunak"
kolom_pencarian.send_keys(kata_kunci)

# Menyimulasikan penekanan tombol Enter pada keyboard
kolom_pencarian.send_keys(Keys.RETURN)

time.sleep(4)

# Mencari elemen judul artikel utama (menggunakan ID "firstHeading")
judul_artikel = browser.find_element(By.ID, "firstHeading").text

print(f"✨ Pengujian Sukses! Artikel yang berhasil dibuka berjudul: '{judul_artikel}'")

time.sleep(2)
browser.quit()