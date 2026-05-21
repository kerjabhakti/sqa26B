import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run_login_test():
    import os
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Hapus tanda pagar jika ingin berjalan tanpa visual browser
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # --- AUTO-DETECT CHROME PATH (Mengatasi 'cannot find Chrome binary') ---
    # Jika Google Chrome diinstal di lokasi kustom atau non-standar, 
    # Anda bisa uncomment & sesuaikan path di bawah ini secara manual:
    # options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            options.binary_location = path
            print(f"Menemukan Chrome binary di: {path}")
            break

    # Mencoba mengimpor webdriver_manager agar user tidak perlu download ChromeDriver manual
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service
        print("Menggunakan webdriver_manager untuk mengunduh/mencocokkan ChromeDriver otomatis...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except ImportError:
        print("webdriver_manager tidak ditemukan, mencoba menjalankan ChromeDriver lokal yang terinstal...")
        driver = webdriver.Chrome(options=options)

    # Menggunakan blok try-finally untuk memastikan browser ditutup sekalipun ada error
    try:
        url = "https://digital-marketplace-solid-frontend.vercel.app/login"
        print(f"Membuka URL: {url}")
        driver.get(url)

        # WebDriverWait untuk memastikan SolidJS selesai merender komponen (maksimal tunggu 15 detik)
        wait = WebDriverWait(driver, 15)

        # 1. Mencari input Email dengan berbagai selector alternatif (agar lebih tangguh)
        print("Mencari field input Email...")
        email_selectors = [
            (By.XPATH, "//label[contains(text(), 'Email')]/..//input"),
            (By.XPATH, "//input[contains(@placeholder, 'example.com')]"),
            (By.NAME, "email"),
            (By.ID, "email"),
            (By.XPATH, "//input[@type='email']"),
        ]
        
        email_input = None
        for by, val in email_selectors:
            try:
                email_input = wait.until(EC.presence_of_element_located((by, val)))
                print(f"-> Ditemukan input Email via: {by} = '{val}'")
                break
            except Exception:
                continue
        
        if not email_input:
            raise Exception("Gagal menemukan field input Email.")

        # 2. Mencari input Password dengan berbagai selector alternatif
        print("Mencari field input Password...")
        password_selectors = [
            (By.XPATH, "//label[contains(text(), 'Password')]/..//input"),
            (By.XPATH, "//input[@type='password']"),
            (By.NAME, "password"),
            (By.ID, "password"),
        ]

        password_input = None
        for by, val in password_selectors:
            try:
                password_input = wait.until(EC.presence_of_element_located((by, val)))
                print(f"-> Ditemukan input Password via: {by} = '{val}'")
                break
            except Exception:
                continue

        if not password_input:
            raise Exception("Gagal menemukan field input Password.")

        # 3. Mencari tombol Login/Submit
        print("Mencari tombol Login...")
        button_selectors = [
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Masuk') or contains(text(), 'login') or contains(text(), 'Sign In') or contains(text(), 'Masuk Sekarang')]"),
        ]

        login_button = None
        for by, val in button_selectors:
            try:
                login_button = wait.until(EC.element_to_be_clickable((by, val)))
                print(f"-> Ditemukan tombol Login via: {by} = '{val}'")
                break
            except Exception:
                continue

        if not login_button:
            raise Exception("Gagal menemukan tombol Login.")

        # 4. Memasukkan kredensial admin
        print("Mengisi kredensial login...")
        email_input.clear()
        email_input.send_keys("admin@gmail.com")
        
        password_input.clear()
        password_input.send_keys("admin1234")

        # 5. Klik login
        print("Mengklik tombol Login...")
        login_button.click()

        # 6. Tunggu loading pasca-login
        print("Menunggu proses login (5 detik)...")
        time.sleep(5)

        # Verifikasi hasil login
        current_url = driver.current_url
        print(f"URL Akhir: {current_url}")
        
        if "login" not in current_url.lower():
            print("\n=== TEST PASSED: Login Berhasil! URL telah dialihkan ===")
        else:
            # Cari pesan error jika ada
            try:
                error_msg = driver.find_element(By.XPATH, "//*[contains(text(), 'invalid') or contains(text(), 'salah') or contains(text(), 'gagal') or contains(text(), 'failed')]")
                print(f"\n=== TEST FAILED: Gagal Login! Pesan di halaman: '{error_msg.text}' ===")
            except:
                print("\n=== TEST WARNING: Masih berada di halaman login. Cek kredensial atau kondisi jaringan. ===")

    except Exception as e:
        print(f"\n[ERROR] Terjadi kesalahan: {e}")
    
    finally:
        print("Menutup browser...")
        driver.quit()

if __name__ == "__main__":
    run_login_test()