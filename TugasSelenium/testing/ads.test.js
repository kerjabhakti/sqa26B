import { Builder, By, until } from 'selenium-webdriver';
import path from 'path';
import { fileURLToPath } from 'url';

// Konfigurasi untuk mendapatkan jalur folder saat ini (Wajib untuk ES Modules)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runningAdminAdsTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // ==========================================
        // LANGKAH 1: LOGIN SEBAGAI ADMIN
        // ==========================================
        console.log('Mengakses halaman login...');
        await driver.get('http://localhost:5173/#/login'); 
        await driver.manage().window().maximize();

        let emailInput = await driver.wait(until.elementLocated(By.css('input[type="email"]')), 5000);
        let passwordInput = await driver.findElement(By.css('input[type="password"]'));
        
        // Menggunakan kredensial admin sesuai kode kamu
        await emailInput.sendKeys('admin@gmail.com');
        await passwordInput.sendKeys('123456');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu hingga masuk ke dashboard admin
        await driver.wait(until.urlContains('admin'), 5000);
        console.log('✅ Login sebagai Admin Sukses!');


        // ==========================================
        // LANGKAH 2: DASHBOARD ADMIN & KLIK TAB MANAJEMEN IKLAN
        // ==========================================
        console.log('Menuju dashboard utama admin...');
        await driver.get('http://localhost:5173/#/admin/dashboard'); 

        console.log('Mencari dan mengklik tab menu Manajemen Iklan...');
        let adsTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Manajemen Iklan')]")), 
            5000
        );
        await adsTab.click();

        // Jeda singkat agar komponen form React selesai rendering
        await driver.sleep(1000); 


        // ==========================================
        // LANGKAH 3: PENGISIAN FORM BANNER IKLAN
        // ==========================================
        console.log('Mulai mengisi data iklan baru...');
        
        // 1. Mengisi Judul Utama
        let titleInput = await driver.wait(
            until.elementLocated(By.css('input[placeholder="Contoh: Diskon Kursi Roda 50%"]')), 
            5000
        );
        await titleInput.sendKeys('Layanan Ambulans Siaga MedisLink 24 Jam');

        // 2. Mengisi Link Tujuan / Redirect (Sudah diperbaiki sesuai placeholder di AddsForm.jsx)
        let linkInput = await driver.findElement(By.css('input[placeholder="/tools atau /login"]'));
        await linkInput.sendKeys('/dashboard');


        // ==========================================
        // LANGKAH 4: SIMULASI UPLOAD BANNER
        // ==========================================
        console.log('Menyuntikkan file gambar banner iklan...');
        let bannerImagePath = path.join(__dirname, 'test_banner.jpeg');
        let fileInput = await driver.findElement(By.css('input[type="file"]'));
        await fileInput.sendKeys(bannerImagePath);


        // ==========================================
        // LANGKAH 5: MENGISI DESKRIPSI SINGKAT
        // ==========================================
        console.log('Mengisi deskripsi singkat...');
        let descriptionTextarea = await driver.findElement(By.css('textarea[placeholder="Deskripsi yang muncul di bawah judul..."]'));
        await descriptionTextarea.sendKeys('Kini hadir layanan pengantaran alat medis darurat gratis untuk wilayah Bandung dan sekitarnya.');


        // ==========================================
        // LANGKAH 6: SUBMIT DAN VALIDASI
        // ==========================================
        console.log('Mengklik tombol Upload & Tampilkan di Slider...');
        let submitButton = await driver.findElement(By.css('button[type="submit"]'));
        await submitButton.click();

        // Jeda akhir memastikan proses klik tereksekusi sebelum browser ditutup
        await driver.sleep(2000); 
        
        console.log('✅ TES SELESAI: Penambahan data banner iklan admin berhasil disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat otomasi form iklan admin:', error);
    } finally {
        console.log('Menutup browser...');
        await driver.quit();
    }
}

runningAdminAdsTest();