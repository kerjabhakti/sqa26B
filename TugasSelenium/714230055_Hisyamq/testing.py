import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inisialisasi WebDriver
driver = webdriver.Chrome()

# Membuka halaman web Google
driver.get("https://www.google.com")

# Menunggu dan mencari elemen input pencarian menggunakan atribut NAME "q"
wait = WebDriverWait(driver, 10)
search_input = wait.until(EC.presence_of_element_located((By.NAME, "q")))

# Memasukkan kata kunci pencarian
search_input.send_keys("kampus digital masa gitu")

# Menekan tombol Enter untuk melakukan pencarian
search_input.send_keys(Keys.ENTER)

# Menunggu hingga hasil pencarian muncul di tampilan halaman (elemen div 'search' milik Google)
wait.until(EC.presence_of_element_located((By.ID, "search")))
print("Hasil pencarian berhasil dimuat.")

# Anda dapat melanjutkan dengan mengambil tindakan lain pada halaman yang terbuka
# Aksi: Mengklik hasil pencarian pertama
try:
    print("Mencari hasil pertama untuk diklik...")
    # Mencari judul tautan pertama (elemen h3) dan memastikan bisa diklik
    first_result = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h3")))
    first_result.click()
    
    # Tunggu beberapa saat agar website tujuan dimuat
    time.sleep(5)
except Exception as e:
    print("Terjadi kesalahan saat mengklik:", e)

# Dapatkan judul halaman web yang telah dibuka
page_title = driver.title
print("Judul halaman saat ini:", page_title)

# Jeda 3 detik agar pengguna dapat melihat tampilan hasil di browser sebelum program selesai
time.sleep(3)

# Menutup WebDriver
driver.quit()