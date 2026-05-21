from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Menggunakan webdriver-manager agar tidak perlu repot setting path ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

try:
    # UBAH BAGIAN INI: Arahkan ke localhost Flask, bukan ke file D:/
    driver.get("http://127.0.0.1:5000/")

    # Memberi waktu sejenak agar halaman termuat sepenuhnya
    time.sleep(2)

    # Input data ke form
    driver.find_element(By.ID, "judul").send_keys("Belajar Pengujian Perangkat Lunak")
    driver.find_element(By.ID, "penulis").send_keys("Dwi Puspa Firdaus")
    driver.find_element(By.ID, "tahun_terbit").send_keys("2024")

    # Jeda sebentar untuk melihat data yang diketik
    time.sleep(1)

    # Klik tombol simpan
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # Tunggu response setelah disubmit
    time.sleep(3)

    print("✅ Mantap! Data berhasil diuji dan disubmit menggunakan Selenium.")
    
except Exception as e:
    print(f"❌ Terjadi kesalahan: {e}")

finally:
    # Menutup browser
    driver.quit()