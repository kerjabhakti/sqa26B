import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class GlowlyAuthTest(unittest.TestCase):
    """
    Test Suite Otomatisasi Pengujian Formal menggunakan Selenium WebDriver (Python unittest).
    Fokus Pengujian: Fitur Registrasi dan Login (Halaman Register & Login) Aplikasi Skincare Reminder (Glowly).
    
    Identitas Mahasiswa:
    - Nama: Aqila Zafira
    - NPM: 714230068
    - Kelas: D4 Teknik Informatika / Sistem Informasi
    """

    @classmethod
    def setUpClass(cls):
        # Base URL server Flask lokal. Pastikan aplikasi Flask Anda sudah berjalan sebelum menjalankan test ini.
        cls.base_url = "http://127.0.0.1:5000"

    def setUp(self):
        # -- 1. INISIALISASI WEBDRIVER BROWSER (SETUP) --
        options = webdriver.ChromeOptions()
        
        # Opsi di bawah ini dapat diaktifkan jika ingin menjalankan pengujian secara 'Headless' (tanpa GUI/tampilan window)
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        
        # Membuka Chrome browser
        self.driver = webdriver.Chrome(options=options)
        
        # Memaksimalkan jendela browser
        self.driver.maximize_window()
        
        # Inisialisasi helper Explicit Wait dengan timeout maksimal 10 detik
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        # -- 2. PEMBERSIHAN BROWSER (TEARDOWN) --
        # Menutup instance browser secara bersih setelah setiap test case dijalankan
        if self.driver:
            self.driver.quit()

    # =========================================================================
    #                    SKENARIO PENGUJIAN: REGISTRASI (REGISTER)
    # =========================================================================

    def test_reg_001_success(self):
        """TC_REG_001: Registrasi Berhasil dengan Data Valid (Skenario Positif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")
        
        # Validasi awal: Memastikan halaman dimuat dengan benar berdasarkan Judul Halaman
        self.wait.until(EC.title_is("Glowly - Register"))

        # Menggenerasi data dinamis (timestamp) agar pendaftaran selalu sukses (idempotent)
        timestamp = int(time.time())
        unique_username = f"user_{timestamp}"
        unique_email = f"user_{timestamp}@gmail.com"
        valid_password = "SecurePassword123!"

        # Menemukan elemen-elemen form input menggunakan locator 'By.NAME'
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        submit_button = driver.find_element(By.CLASS_NAME, "register-btn")

        # Menginput data ke form registrasi
        email_field.send_keys(unique_email)
        username_field.send_keys(unique_username)
        password_field.send_keys(valid_password)
        confirm_password_field.send_keys(valid_password)
        
        # Mengeklik tombol daftar
        submit_button.click()

        # ASSERTION 1: Memastikan URL dialihkan (redirect) secara otomatis ke Halaman Login
        self.wait.until(EC.url_contains("/login"))
        self.assertIn("/login", driver.current_url.lower(), "Registrasi sukses seharusnya dialihkan ke halaman login.")

        # ASSERTION 2: Memastikan muncul pesan sukses (flash message) dari server Flask
        flash_message = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "flash-message")))
        self.assertIn("Registration successful. Please log in.", flash_message.text, 
                      "Pesan flash registrasi sukses tidak muncul atau tidak sesuai.")

    def test_reg_002_failed_invalid_email(self):
        """TC_REG_002: Registrasi Gagal karena Format Email Tidak Valid (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")

        # Menemukan elemen form input
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        submit_button = driver.find_element(By.CLASS_NAME, "register-btn")

        # Input data dengan email berformat salah
        email_field.send_keys("email_tidak_valid")
        username_field.send_keys("usertest")
        password_field.send_keys("Password123")
        confirm_password_field.send_keys("Password123")
        
        # Klik tombol daftar
        submit_button.click()

        # ASSERTION: Validasi HTML5 client-side memblokir pengiriman form
        # Karena input bertipe 'email', browser Chromium otomatis memblokir POST request jika format salah.
        is_valid = driver.execute_script("return arguments[0].validity.valid;", email_field)
        self.assertFalse(is_valid, "Validasi form browser HTML5 seharusnya mendeteksi format email salah.")

    def test_reg_003_failed_password_mismatch(self):
        """TC_REG_003: Registrasi Gagal karena Konfirmasi Sandi Tidak Cocok (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")

        # Menemukan elemen form input
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        submit_button = driver.find_element(By.CLASS_NAME, "register-btn")

        # Input data dengan kata sandi & konfirmasi kata sandi yang berbeda
        email_field.send_keys("validuser@gmail.com")
        username_field.send_keys("validuser")
        password_field.send_keys("Password123")
        confirm_password_field.send_keys("Password456")  # Beda dengan password utama
        
        # Klik daftar
        submit_button.click()

        # ASSERTION 1: Memastikan halaman tidak diarahkan ke halaman login (tetap di register)
        self.assertIn("/register", driver.current_url.lower())

        # ASSERTION 2: Memvalidasi pesan galat pencocokan kata sandi dari backend Flask
        error_flash = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "flash-message")))
        self.assertIn("Passwords do not match", error_flash.text, 
                      "Pesan kesalahan konfirmasi sandi tidak sesuai.")

    def test_reg_004_failed_username_exists(self):
        """TC_REG_004: Registrasi Gagal karena Username Sudah Terdaftar (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")

        # Menemukan elemen form input
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        username_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        confirm_password_field = driver.find_element(By.NAME, "confirm_password")
        submit_button = driver.find_element(By.CLASS_NAME, "register-btn")

        # Menginput username yang sudah ada di database (seeded: 'testuser1')
        email_field.send_keys("email_baru_sekali@gmail.com")
        username_field.send_keys("testuser1")  # Sudah terdaftar
        password_field.send_keys("Password123")
        confirm_password_field.send_keys("Password123")
        
        # Klik daftar
        submit_button.click()

        # ASSERTION: Validasi backend Flask menolak pendaftaran dan mengirimkan pesan galat terdaftar
        error_flash = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "flash-message")))
        self.assertIn("Username already exists", error_flash.text, 
                      "Pesan kesalahan duplikasi username tidak terdeteksi.")

    def test_reg_005_failed_empty_fields(self):
        """TC_REG_006: Registrasi Gagal karena Membiarkan Kolom Wajib Kosong (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/register")

        # Menemukan field email wajib diisi
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        submit_button = driver.find_element(By.CLASS_NAME, "register-btn")

        # Klik daftar tanpa mengisi formulir
        submit_button.click()

        # ASSERTION: Validasi HTML5 client-side mendeteksi input kosong dan memblokir pengiriman ke server
        # Elemen input email harus memiliki atribut 'required' yang bernilai true/aktif
        is_required = email_field.get_attribute("required")
        self.assertTrue(is_required, "Field email wajib diisi namun atribut 'required' tidak aktif.")
        
        # Cek status validity valueMissing (kosong pada field required) menggunakan Javascript
        value_missing = driver.execute_script("return arguments[0].validity.valueMissing;", email_field)
        self.assertTrue(value_missing, "Browser harus memicu error 'valueMissing' karena kolom email dikosongkan.")


    # =========================================================================
    #                        SKENARIO PENGUJIAN: LOGIN
    # =========================================================================

    def test_log_001_success_user(self):
        """TC_LOG_001: Login Berhasil sebagai User Biasa (Skenario Positif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Menemukan elemen login form input dengan locator 'By.NAME'
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CLASS_NAME, "login-btn")

        # Menginput kredensial user biasa valid (seeded: 'testuser2' / 'password')
        username_field.send_keys("testuser2")
        password_field.send_keys("password")
        
        # Klik masuk
        submit_button.click()

        # ASSERTION 1: Memastikan URL dialihkan secara tepat ke Halaman Beranda utama ('/')
        self.wait.until(EC.url_to_be(f"{self.base_url}/"))
        self.assertEqual(driver.current_url, f"{self.base_url}/", "User biasa gagal diarahkan ke halaman beranda utama.")

        # ASSERTION 2: Memastikan Judul Halaman berubah menjadi Beranda
        self.assertEqual(driver.title, "Glowly - Beranda", "Judul halaman beranda setelah login salah.")

    def test_log_002_success_admin(self):
        """TC_LOG_002: Login Berhasil sebagai Administrator (Skenario Positif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Menemukan elemen form input
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CLASS_NAME, "login-btn")

        # Menginput kredensial admin valid (seeded: 'testuser1' / 'password')
        username_field.send_keys("testuser1")
        password_field.send_keys("password")
        
        # Klik masuk
        submit_button.click()

        # ASSERTION 1: Memastikan URL dialihkan secara tepat ke Halaman Dasbor Admin ('/admin')
        self.wait.until(EC.url_contains("/admin"))
        self.assertIn("/admin", driver.current_url, "Administrator gagal diarahkan ke dasbor admin.")

        # ASSERTION 2: Memastikan Judul Halaman berubah menjadi Dasbor Admin
        self.assertEqual(driver.title, "Glowly - Dasbor Admin", "Judul halaman dasbor admin setelah login salah.")

    def test_log_003_failed_wrong_password(self):
        """TC_LOG_003: Login Gagal karena Kata Sandi Salah (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Menemukan elemen form input
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        submit_button = driver.find_element(By.CLASS_NAME, "login-btn")

        # Menginput kredensial dengan password salah
        username_field.send_keys("testuser2")
        password_field.send_keys("password_salah")  # Salah
        
        # Klik masuk
        submit_button.click()

        # ASSERTION 1: Memastikan tetap berada di halaman login
        self.assertIn("/login", driver.current_url.lower())

        # ASSERTION 2: Memvalidasi pesan galat flash dari server Flask
        error_flash = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "flash-message")))
        self.assertIn("Invalid email or password", error_flash.text, 
                      "Pesan kesalahan login tidak muncul atau tidak sesuai.")

    def test_log_004_failed_empty_fields(self):
        """TC_LOG_005: Login Gagal karena Membiarkan Kolom Wajib Kosong (Skenario Negatif)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Menemukan input username yang wajib diisi
        username_field = self.wait.until(EC.presence_of_element_located((By.NAME, "username")))
        submit_button = driver.find_element(By.CLASS_NAME, "login-btn")

        # Klik submit langsung tanpa mengisi field username
        submit_button.click()

        # ASSERTION: Validasi HTML5 client-side mendeteksi input kosong dan memblokir pengiriman ke server
        is_required = username_field.get_attribute("required")
        self.assertTrue(is_required, "Field username wajib diisi namun atribut 'required' tidak aktif.")
        
        # Cek validity browser
        value_missing = driver.execute_script("return arguments[0].validity.valueMissing;", username_field)
        self.assertTrue(value_missing, "Browser harus memicu error 'valueMissing' karena kolom username dikosongkan.")

    def test_log_005_toggle_password_visibility(self):
        """TC_LOG_006: Menguji Fitur Tampilkan/Sembunyikan Sandi (Show/Hide Password)"""
        driver = self.driver
        driver.get(f"{self.base_url}/login")

        # Menemukan elemen input password dan tombol toggle mata
        password_field = self.wait.until(EC.presence_of_element_located((By.NAME, "password")))
        toggle_button = driver.find_element(By.CLASS_NAME, "toggle-password")

        # Input data ke field password
        password_field.send_keys("UjiPassword123")

        # ASSERTION 1: Secara default, tipe input adalah 'password' (karakter disamarkan)
        self.assertEqual(password_field.get_attribute("type"), "password", 
                         "Default type field password seharusnya adalah 'password'.")

        # Tindakan: Klik ikon mata untuk menampilkan password
        toggle_button.click()

        # ASSERTION 2: Tipe input berubah menjadi 'text' (karakter terlihat)
        self.assertEqual(password_field.get_attribute("type"), "text", 
                         "Tipe field password gagal diubah menjadi 'text' setelah diklik.")

        # Tindakan: Klik ikon mata kembali untuk menyembunyikan password
        toggle_button.click()

        # ASSERTION 3: Tipe input kembali menjadi 'password' (karakter disamarkan ulang)
        self.assertEqual(password_field.get_attribute("type"), "password", 
                         "Tipe field password gagal diubah kembali menjadi 'password'.")


if __name__ == "__main__":
    unittest.main()
