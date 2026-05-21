import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Inisialisasi WebDriver
driver = webdriver.Chrome()

# Membuka halaman web Nyumbangin
driver.get("https://www.nyumbangin.web.id/")

# Tambahkan penundaan waktu untuk memastikan halaman fully loaded
time.sleep(5)

# Mengambil judul halaman
page_title = driver.title
print("Judul halaman:", page_title)

# Mengambil URL halaman saat ini
current_url = driver.current_url
print("URL halaman:", current_url)

# Mencari tombol "Mulai Sekarang" atau elemen utama di halaman
try:
    # Cari heading yang berisi "Buat Halaman Donasi Pribadi Anda"
    heading = driver.find_element(By.TAG_NAME, "h1")
    print("Heading utama:", heading.text)
except:
    print("Heading tidak ditemukan")

# Mencari jumlah creator yang terdaftar (cari elemen yang menampilkan daftar creator)
try:
    # Cari semua link creator
    creator_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/donate/')]")
    
    # Ambil username unik (remove duplicates)
    unique_creators = set()
    for creator in creator_links:
        href = creator.get_attribute("href")
        if href and "/donate/" in href:
            username = href.split("/donate/")[-1].strip()
            if username:
                unique_creators.add(username)
    
    print(f"Jumlah creator UNIK: {len(unique_creators)}")
    
    # Tampilkan beberapa creator unik
    if unique_creators:
        print("\nBeberapa creator unik:")
        for i, username in enumerate(sorted(list(unique_creators))[:10]):
            print(f"  - {username}")
except Exception as e:
    print(f"Gagal mengambil data creator: {e}")

# Mengecek apakah tombol "Mulai Sekarang" tersedia
try:
    start_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Mulai Sekarang')]")
    print(f"\nTombol 'Mulai Sekarang' ditemukan: {start_button.is_displayed()}")
except:
    print("Tombol 'Mulai Sekarang' tidak ditemukan")

# Mengecek halaman terutama body element yang ada
print(f"\nStatus: Halaman berhasil dimuat dengan sukses!")
print(f"Ukuran window: {driver.get_window_size()}")

# Menutup WebDriver
driver.quit()
