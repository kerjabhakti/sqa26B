import { Builder, By, until } from 'selenium-webdriver';
import path from 'path';
import { fileURLToPath } from 'url';

// Konfigurasi untuk mendapatkan jalur folder saat ini (Wajib untuk ES Modules)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runningAdminNewsTest() {
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
        
        // Gunakan kredensial admin kamu
        await emailInput.sendKeys('admin@gmail.com');
        await passwordInput.sendKeys('123456');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu hingga masuk ke dashboard admin
        await driver.wait(until.urlContains('admin'), 5000);
        console.log('✅ Login sebagai Admin Sukses!');


        // ==========================================
        // LANGKAH 2: DASHBOARD ADMIN & KLIK TAB BERITA
        // ==========================================
        console.log('Menuju dashboard utama admin...');
        await driver.get('http://localhost:5173/#/admin/dashboard'); 

        console.log('Mencari dan mengklik tab menu Berita...');
        // Mencari elemen tab menu atas berdasarkan teks "Berita"
        let newsTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Berita')]")), 
            5000
        );
        await newsTab.click();

        // Jeda singkat memastikan komponen form berita selesai di-render
        await driver.sleep(1000); 


        // ==========================================
        // LANGKAH 3: PENGISIAN DATA FORM BERITA
        // ==========================================
        console.log('Mulai mengisi form artikel berita baru...');
        
        // 1. Mengisi Judul Berita (Ditembak berdasarkan placeholder)
        let titleInput = await driver.wait(
            until.elementLocated(By.css('input[placeholder="Contoh: Kegiatan Donor Darah 2024"]')), 
            5000
        );
        await titleInput.sendKeys('Kolaborasi MedisLink dan PMI: Aksi Donor Darah Serentak');


        // ==========================================
        // LANGKAH 4: SIMULASI UPLOAD SAMPUL BERITA
        // ==========================================
        console.log('Menyuntikkan file gambar sampul berita...');
        let newsImagePath = path.join(__dirname, 'news_test.png');
        let fileInput = await driver.findElement(By.css('input[type="file"]'));
        await fileInput.sendKeys(newsImagePath);


        // ==========================================
        // LANGKAH 5: MENGISI KONTEN UTAMA BERITA
        // ==========================================
        console.log('Mengisi konten detail berita...');
        let contentTextarea = await driver.findElement(By.css('textarea[placeholder="Tulis detail berita lengkap di sini..."]'));
        await contentTextarea.sendKeys(
            'MedisLink bekerja sama dengan Palang Merah Indonesia (PMI) akan menyelenggarakan kegiatan donor darah serentak. ' +
            'Kegiatan ini bertujuan untuk memenuhi stok kebutuhan darah linear penunjang rumah sakit darurat di kota Bandung. ' +
            'Bagi warga yang bersedia berpartisipasi dapat langsung mendatangi posko utama sekretariat terdekat pada akhir pekan ini.'
        );


        // ==========================================
        // LANGKAH 6: SUBMIT FORM BERITA
        // ==========================================
        console.log('Mengklik tombol Publikasikan Berita...');
        let submitButton = await driver.findElement(By.css('button[type="submit"]'));
        await submitButton.click();

        // Jeda pengunci memastikan request FormData dikirim seutuhnya sebelum browser ditutup
        await driver.sleep(2500); 
        
        console.log('✅ TES SELESAI: Simulasi publikasi berita baru sisi admin sukses total!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat otomasi form manajemen berita:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningAdminNewsTest();