import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Menyiapkan dan membuka browser Chrome
browser = webdriver.Chrome()

# Mengakses halaman utama Wikipedia Bahasa Indonesia
browser.get("https://id.wikipedia.org/")

#  Menemukan kolom pencarian Wikipedia (menggunakan atribut NAME "search")
kolom_pencarian = browser.find_element(By.NAME, "search")

kata_kunci = "Pengujian perangkat lunak"
kolom_pencarian.send_keys(kata_kunci)

# Menyimulasikan penekanan tombol Enter pada keyboard
kolom_pencarian.send_keys(Keys.RETURN)

time.sleep(4)

# Mencari elemen judul artikel utama (menggunakan ID "firstHeading") dan mengambil teksnya
judul_artikel = browser.find_element(By.ID, "firstHeading").text

print(f"✨ Pengujian Sukses! Artikel yang berhasil dibuka berjudul: '{judul_artikel}'")

browser.quit()