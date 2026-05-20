from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# 1. Inisialisasi WebDriver (Contoh menggunakan Chrome)
driver = webdriver.Chrome()

try:
    # 2. Buka halaman login KaryaKlik
    driver.get("https://karyaklik.netlify.app/login")
    driver.maximize_window()
    
    # Berikan waktu eksplisit untuk memastikan halaman termuat
    wait = WebDriverWait(driver, 10)
    
    print("--- Memulai Test Skenario 1: Login Form Manual ---")
    
    # 3. Cari elemen input Email dan Password
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your email']")))
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Enter your password']")
    login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login to KaryaKlik')]")
    
    # 4. Masukkan data uji (Ubah sesuai dengan akun test Anda)
    email_input.clear()
    email_input.send_keys("karyaklik@gmail.com")
    
    password_input.clear()
    password_input.send_keys("admin123")
    
    # 5. Klik tombol login
    login_button.click()
    print("Skenario 1: Form login berhasil diisi dan diklik.")
    
    # Berikan jeda untuk melihat hasil/redirect
    time.sleep(10)
    
    # --- Skenario Tambahan: Klik Google Sign-In ---
    # Karena Google Sign-In berada di dalam iframe (berdasarkan struktur page), 
    # kita perlu beralih ke iframe tersebut terlebih dahulu jika ingin mengkliknya.
    
    print("\n--- Memulai Test Skenario 2: Interaksi Google Sign-In ---")
    # Kembali ke halaman login utama untuk demonstrasi tombol Google
    driver.get("https://karyaklik.netlify.app/login")
    
    # Switch ke iframe pihak ketiga (Google Sign-In)
    # Mencari iframe yang mengandung src/title terkait Google Accounts
    google_iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'Sign In - Google Accounts')]")))
    driver.switch_to.frame(google_iframe)
    
    # Klik area profil Google yang tersedia (Viola Septianti)
    google_profile_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign in as Viola Septianti')]")))
    google_profile_btn.click()
    print("Skenario 2: Tombol Google Sign-In berhasil diklik.")
    
    # Keluar dari iframe kembali ke konteks halaman utama
    driver.switch_to.default_content()
    
    time.sleep(5)

except Exception as e:
    print(f"Terjadi error saat pengujian: {e}")

finally:
    # 6. Tutup browser setelah selesai
    driver.quit()
    print("\nPengujian selesai, browser ditutup.")