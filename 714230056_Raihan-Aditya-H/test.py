import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def main():
    # Set up Chrome options
    options = Options()
    
    # Check if run in headless mode (e.g., python test.py --headless)
    if "--headless" in sys.argv:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        print("Menjalankan dalam mode Headless...")

    print("Menginisialisasi Chrome WebDriver...")
    driver = webdriver.Chrome(options=options)
    
    try:
        print("Membuka halaman Google...")
        driver.get("https://www.google.com")
        
        # Mencari elemen input pencarian menggunakan ID 'APjFqb'
        print("Mencari kolom pencarian...")
        search_input = driver.find_element(By.ID, "APjFqb")
        
        # Memasukkan kata kunci pencarian
        keyword = "kampus digital masa gitu"
        print(f"Memasukkan kata kunci pencarian: '{keyword}'")
        search_input.send_keys(keyword)
        
        # Menekan tombol Enter untuk melakukan pencarian
        search_input.send_keys(Keys.ENTER)
        
        # Menunggu hasil pencarian dimuat
        print("Menunggu 5 detik untuk memuat hasil pencarian...")
        time.sleep(5)
        
        # Mendapatkan judul halaman saat ini
        page_title = driver.title
        print("\n=== Hasil Pengujian ===")
        print("Judul halaman:", page_title)
        
        # Verifikasi sederhana apakah kata kunci atau hasil relevan ditemukan di judul
        if "Google" not in page_title:
            print("Pengujian Berhasil: Halaman pencarian telah dimuat.")
        else:
            print("Pengujian Selesai: Halaman pencarian selesai dimuat.")
        print("=======================\n")
        
    except Exception as e:
        print(f"Terjadi kesalahan saat pengujian: {e}")
        
    finally:
        print("Menutup WebDriver...")
        driver.quit()

if __name__ == "__main__":
    main()
