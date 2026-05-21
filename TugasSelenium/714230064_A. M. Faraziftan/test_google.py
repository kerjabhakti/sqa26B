import os
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = "https://karyaklik.netlify.app"


def get_env_or_prompt(name: str, prompt: str, *, secret: bool = False) -> str:
	value = os.getenv(name)
	if value:
		return value

	if secret:
		value = getpass.getpass(f"{prompt}: ")
	else:
		value = input(f"{prompt}: ").strip()

	if not value:
		raise RuntimeError(
			f"Nilai untuk '{name}' kosong. Set environment variable atau isi saat prompt."
		)
	return value

email = get_env_or_prompt("KARYAKLIK_EMAIL", "Masukkan email KaryaKlik")
password = get_env_or_prompt(
	"KARYAKLIK_PASSWORD", "Masukkan password KaryaKlik (tidak akan ditampilkan)", secret=True
)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)

try:
	wait = WebDriverWait(driver, 15)

	driver.get(f"{BASE_URL}/login")

	email_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='email']")))
	password_input = wait.until(
		EC.visibility_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
	)

	email_input.clear()
	email_input.send_keys(email)

	password_input.clear()
	password_input.send_keys(password)

	submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
	submit_button.click()

	try:
		wait.until(EC.url_changes(f"{BASE_URL}/login"))
		print("Login diklik dan URL berubah (indikasi login berhasil / redirect terjadi).")
		print("URL sekarang:", driver.current_url)
	except Exception:
		print("Login sudah dicoba, tapi URL belum berubah.")
		print("URL sekarang:", driver.current_url)
		page_text = driver.find_element(By.TAG_NAME, "body").text
		if "invalid" in page_text.lower() or "error" in page_text.lower() or "failed" in page_text.lower():
			print("Terlihat ada pesan error pada halaman.")

finally:
	driver.quit()