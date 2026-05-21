from urllib.parse import quote_plus

import time

from selenium import webdriver
from selenium.common.exceptions import WebDriverException


# Keyword pencarian ditulis langsung di dalam kode.
keyword = "kampus digital masa gitu"

driver = None

try:
    # Selenium Manager biasanya akan membantu mencari ChromeDriver secara otomatis.
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # Membuka browser Google Chrome.
    driver = webdriver.Chrome(options=options)

    # Mengakses halaman Google terlebih dahulu.
    driver.get("https://www.google.com")
    time.sleep(2)

    # Melakukan pencarian dengan keyword yang sudah ditulis di kode.
    search_url = f"https://www.google.com/search?q={quote_plus(keyword)}"
    driver.get(search_url)
    time.sleep(3)

    # Mengambil judul halaman hasil pencarian.
    title_halaman = driver.title
    print("Judul halaman:", title_halaman)

except WebDriverException as error:
    print("Terjadi error pada Selenium atau Chrome:", error)
except Exception as error:
    print("Terjadi error tidak terduga:", error)
finally:
    # Menutup browser setelah program selesai.
    if driver is not None:
        time.sleep(1)
        driver.quit()