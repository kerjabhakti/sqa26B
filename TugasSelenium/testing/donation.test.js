import { Builder, By, until } from 'selenium-webdriver';
import path from 'path';
import { fileURLToPath } from 'url';

// Konfigurasi untuk mendapatkan jalur folder saat ini (wajib untuk ES Modules Node.js)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runningDonationTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // ==========================================
        // LANGKAH 1: LOGIN KE SISTEM MEDISLINK
        // ==========================================
        console.log('Mengakses halaman login...');
        await driver.get('http://localhost:5173/#/login'); 
        await driver.manage().window().maximize();

        // Cari input email dan password berdasarkan tipe komponen
        let emailInput = await driver.wait(until.elementLocated(By.css('input[type="email"]')), 5000);
        let passwordInput = await driver.findElement(By.css('input[type="password"]'));
        
        // Masukkan kredensial akun testing yang valid di database/sistem kamu
        await emailInput.sendKeys('aghniihsn@gmail.com');
        await passwordInput.sendKeys('123456');
        
        console.log('Mengklik tombol submit login...');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu sampai login sukses dan masuk ke halaman dashboard utama
        await driver.wait(until.urlContains('dashboard'), 5000);
        console.log('✅ Login Sukses!');


        // ==========================================
        // LANGKAH 2: KLIK TAB MENU DONASI ALAT MEDIS
        // ==========================================
        console.log('Mencari dan mengklik tab menu Donasi Alat Medis...');
        // Mencari elemen tombol/tab berdasarkan teks yang tertera di layar
        let donationTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Donasi Alat')]")), 
            5000
        );
        await donationTab.click();

        // Berikan jeda singkat agar React selesai memindahkan state tab UI
        await driver.sleep(500); 


        // ==========================================
        // LANGKAH 3: PENGISIAN FORM DONASI ALAT MEDIS
        // ==========================================
        console.log('Mulai mengisi form data donasi...');

        // 1. Mengisi Nama Alat Medis
        let toolNameInput = await driver.wait(until.elementLocated(By.name('tool_name')), 5000);
        await toolNameInput.sendKeys('Kursi Roda Standard Modifikasi');

        // 2. Memilih Kategori (Dropdown)
        let categorySelect = await driver.findElement(By.name('category'));
        await categorySelect.sendKeys('Mobilitas (Kursi Roda, Tongkat, dll)');

        // 3. Mengisi Deskripsi Kondisi & Spesifikasi Alat
        let descriptionInput = await driver.findElement(By.name('description'));
        await descriptionInput.sendKeys('Kondisi ban masih bagus, rem berfungsi normal, besi sedikit lecet pemakaian.');

        // 4. Mengisi Jumlah Unit (Hapus angka default '1' bawaan state terlebih dahulu)
        let quantityInput = await driver.findElement(By.name('quantity'));
        await quantityInput.clear(); 
        await quantityInput.sendKeys('2');


        // ==========================================
        // LANGKAH 4: SIMULASI UPLOAD FOTO/GAMBAR ALAT
        // ==========================================
        console.log('Menyuntikkan file gambar ke form upload...');
        // Mengambil letak file 'test_image.png' yang berada di satu folder dengan skrip ini
        let absoluteImagePath = path.join(__dirname, 'image_testing.jpeg');
        let fileInput = await driver.findElement(By.css('input[type="file"]'));
        
        // Kirim absolute path file gambar langsung ke input file tersembunyi
        await fileInput.sendKeys(absoluteImagePath);


        // ==========================================
        // LANGKAH 5: MENGISI TANGGAL & LOKASI BARANG
        // ==========================================
        // 5. Mengisi Rencana Tanggal Penjemputan (Gunakan format YYYY-MM-DD)
        let dateInput = await driver.findElement(By.name('pickup_date'));
        await dateInput.sendKeys('2026-05-25'); 

        // 6. Mengisi Lokasi Alamat Barang
        let addressInput = await driver.findElement(By.name('pickup_address'));
        await addressInput.sendKeys('Jl. Terusan Jenderal Sudirman No. 45, Cimahi, Jawa Barat');


        // ==========================================
        // LANGKAH 6: KIRIM FORM DONASI (SUBMIT)
        // ==========================================
        console.log('Mengklik tombol Kirim Donasi...');
        let submitButton = await driver.findElement(By.css('button[type="submit"]'));
        await submitButton.click();

        // Validasi Akhir: Memastikan sistem memproses input dan tidak stuck/error di halaman form
        // Berdasarkan kode komponenmu, jika sukses akan dialihkan kembali atau me-refresh dashboard
        await driver.wait(until.urlContains('dashboard'), 5000);
        
        console.log('✅ TES SELESAI: Alur login dan pengisian form Donasi MedisLink sukses total!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat proses otomasi:', error);
    } finally {
        // Menutup browser otomatis agar ram laptop tidak penuh
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningDonationTest();