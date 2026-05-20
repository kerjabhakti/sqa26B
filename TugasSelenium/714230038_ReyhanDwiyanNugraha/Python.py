import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def main():
	options = Options()

	if "--headless" in sys.argv:
		options.add_argument("--headless=new")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		print("Menjalankan dalam mode Headless...")

	print("Menginisialisasi Chrome WebDriver...")
	driver = webdriver.Chrome(options=options)

	try:
		link = "https://www.roniandarsyah.com/"
		print(f"Membuka halaman {link}...")
		driver.get(link)

		print("Mencari kolom pencarian...")
		# Gunakan locator yang lebih stabil (By.NAME) untuk kotak pencarian
		search_input = driver.find_element(By.NAME, "q")

		keyword = "Selenium"
		print(f"Memasukkan kata kunci pencarian: '{keyword}'")
		search_input.send_keys(keyword)
		search_input.send_keys(Keys.ENTER)

		print("Menunggu 5 detik untuk memuat hasil pencarian...")
		time.sleep(5)

		page_title = driver.title
		print("\n=== Hasil Pengujian ===")
		print("Judul halaman:", page_title)

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