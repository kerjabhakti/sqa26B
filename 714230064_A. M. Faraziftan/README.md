# Selenium Testing

Pengujian sederhana menggunakan Selenium WebDriver untuk mencoba login ke KaryaKlik (email & password).

## Prasyarat
- Google Chrome ter-install
- Python

## Cara Menjalankan

### Opsi 1: Isi kredensial saat prompt (paling mudah)
```powershell
pip install selenium
python test_google.py
```

### Opsi 2: Pakai environment variable (lebih cepat untuk run berulang)
```powershell
pip install selenium

$env:KARYAKLIK_EMAIL = "hulam@gmail.com"
$env:KARYAKLIK_PASSWORD = "Bismillah2005"

python test_google.py
```

Catatan:
- Password yang diketik di prompt tidak akan ditampilkan (hidden input).
- Selenium biasanya akan mengunduh/menyesuaikan ChromeDriver otomatis (Selenium Manager).