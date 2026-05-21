# Program Selenium Otomatis - Google Search
# Membuka Chrome, searching di Google, ambil title, dan tutup browser

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# Keyword pencarian yang akan digunakan
KEYWORD_PENCARIAN = "kampus digital masa gitu"

try:
    # ===== 1. Inisialisasi Chrome Driver =====
    print("🔄 Membuka browser Google Chrome...")
    
    # Menggunakan webdriver-manager untuk ChromeDriver otomatis
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    print("✅ Browser berhasil dibuka!\n")
    
    # ===== 2. Akses Google.com =====
    print("🌐 Mengakses https://www.google.com...")
    driver.get("https://www.google.com")
    
    # Tunggu halaman selesai dimuat
    time.sleep(2)
    print("✅ Halaman Google berhasil diakses!\n")
    
    # ===== 3. Cari keyword di Google =====
    print(f"🔍 Melakukan pencarian untuk: '{KEYWORD_PENCARIAN}'...")
    
    # Tunggu search box muncul dan masukkan keyword
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    
    search_box.send_keys(KEYWORD_PENCARIAN)
    
    # Tekan Enter untuk melakukan pencarian
    search_box.submit()
    
    # Tunggu hasil pencarian muncul
    time.sleep(2)
    print("✅ Pencarian berhasil dilakukan!\n")
    
    # ===== 4. Ambil dan Tampilkan Judul Halaman =====
    print("📄 Mengambil judul halaman hasil pencarian...")
    
    # Ambil title dari halaman saat ini
    page_title = driver.title
    
    # Tampilkan ke terminal
    print("\n" + "="*60)
    print(f"📌 JUDUL HALAMAN HASIL PENCARIAN:")
    print(f"{page_title}")
    print("="*60 + "\n")
    
    # ===== 5. Tampilkan URL saat ini (bonus) =====
    current_url = driver.current_url
    print(f"🔗 URL saat ini: {current_url}\n")
    
    # Tunggu sebentar untuk user bisa melihat hasil
    time.sleep(2)
    
    # ===== 6. Tutup Browser =====
    print("🔴 Menutup browser...")
    driver.quit()
    print("✅ Browser berhasil ditutup!\n")
    
    print("✨ Program selesai dengan sukses!")

except Exception as e:
    # ===== ERROR HANDLING =====
    print(f"\n❌ TERJADI ERROR: {str(e)}\n")
    print("Informasi Error:")
    print(f"Tipe Error: {type(e).__name__}")
    print(f"Pesan: {str(e)}")
    
    # Pastikan browser ditutup jika terjadi error
    try:
        driver.quit()
        print("\n🔴 Browser ditutup karena terjadi error.")
    except:
        pass

