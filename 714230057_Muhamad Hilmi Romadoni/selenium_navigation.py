import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inisialisasi WebDriver
driver = webdriver.Chrome()

try:
    # 1. Navigasi ke website
    print("=" * 50)
    print("SELENIUM AUTOMATION TEST")
    print("=" * 50)
    
    driver.get("https://www.wikipedia.org")
    print("✓ Membuka Wikipedia")
    time.sleep(2)
    
    # 2. Ambil judul halaman awal
    page_title = driver.title
    print(f"  Judul halaman: {page_title}")
    
    # 3. Cari elemen dan lakukan pencarian
    print("\n→ Melakukan pencarian...")
    search_box = driver.find_element(By.ID, "searchInput")
    search_box.send_keys("Python (programming language)")
    search_box.send_keys(Keys.ENTER)
    print("✓ Pencarian dilakukan")
    time.sleep(3)
    
    # 4. Tunggu halaman hasil pencarian
    wait = WebDriverWait(driver, 10)
    page_heading = wait.until(EC.presence_of_element_located((By.XPATH, "//h1")))
    print(f"✓ Halaman hasil ditemukan: {page_heading.text}")
    
    # 5. Ambil beberapa link dari halaman
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\n→ Total link di halaman: {len(links)}")
    print("  5 link pertama:")
    for i, link in enumerate(links[:5]):
        href = link.get_attribute("href")
        text = link.text
        if href and text:
            print(f"    {i+1}. {text[:40]}")
    
    # 6. Klik link pertama jika ada
    if links:
        for link in links:
            try:
                href = link.get_attribute("href")
                if href and "edit" not in href.lower():
                    link.click()
                    print("\n✓ Link diklik")
                    time.sleep(2)
                    break
            except:
                pass
    
    # 7. Navigasi kembali
    driver.back()
    print("✓ Navigasi kembali")
    time.sleep(2)
    
    # 8. Ambil URL saat ini
    current_url = driver.current_url
    print(f"  URL saat ini: {current_url[:50]}...")
    
    # 9. Tutup warning/notification jika ada
    try:
        close_buttons = driver.find_elements(By.XPATH, "//button[@aria-label='close']")
        if close_buttons:
            close_buttons[0].click()
            print("✓ Notifikasi ditutup")
    except:
        pass
    
    print("\n" + "=" * 50)
    print("✓ TEST SELESAI DENGAN SUKSES")
    print("=" * 50)
    
except Exception as e:
    print(f"\n✗ Terjadi error: {e}")
    import traceback
    traceback.print_exc()

finally:
    # Tutup browser
    time.sleep(2)
    driver.quit()
    print("\n✓ Browser ditutup")
