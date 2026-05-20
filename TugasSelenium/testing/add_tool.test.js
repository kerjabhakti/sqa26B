import { Builder, By, until } from 'selenium-webdriver';
import path from 'path';
import { fileURLToPath } from 'url';

// Konfigurasi jalur folder saat ini (Wajib untuk ES Modules)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runningAddToolTest() {
    // 1. Inisialisasi Browser Chrome
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
        
        await emailInput.sendKeys('admin@gmail.com');
        await passwordInput.sendKeys('123456');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu hingga masuk ke dashboard admin
        await driver.wait(until.urlContains('admin'), 5000);
        console.log('✅ Login Admin Sukses!');


        // ==========================================
        // LANGKAH 2: MASUK KE TAB INVENTARIS & BUKA MODAL
        // ==========================================
        console.log('Menuju dashboard utama admin...');
        await driver.get('http://localhost:5173/#/admin/dashboard'); 

        console.log('Mencari dan mengklik tab menu Inventaris...');
        let inventarisTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Inventaris')]")), 
            5000
        );
        await inventarisTab.click();
        await driver.sleep(500);

        console.log('Memicu kemunculan modal dengan mengklik tombol Tambah Alat...');
        // Cari tombol aksi tambah alat medis yang memicu modal isOpen=true
        let openModalButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Tambah Alat') or contains(., 'Tambah')]")), 
            5000
        );
        await openModalButton.click();


        // ==========================================
        // LANGKAH 3: INTERAKSI DROPDOWN PRESETS DINAMIS
        // ==========================================
        console.log('Memilih Kategori Alat...');
        // Mencari dropdown kategori alat (Dropdown pertama di dalam form modal)
        let selectCategory = await driver.wait(
            until.elementLocated(By.xpath("//select[option[@value='MOBILITAS']]")), 
            5000
        );
        // Kita simulasikan memilih kategori PERNAPASAN
        await selectCategory.sendKeys('PERNAPASAN');
        await driver.sleep(300);

        console.log('Memilih Nama Alat...');
        // Mencari dropdown nama alat (Dropdown kedua yang menampung preset types sesuai kategori)
        let selectToolName = await driver.findElement(By.xpath("//select[option[contains(text(), '-- Pilih Alat --')]]"));
        // Memilih salah satu jenis alat preset kategori PERNAPASAN, misalnya Tabung Oksigen
        await selectToolName.sendKeys('Tabung Oksigen');
        await driver.sleep(500); // Berikan jeda agar label dinamis React ter-update


        // ==========================================
        // LANGKAH 4: PENGISIAN FORM SPESIFIKASI (INDEX-BASED SELECTOR)
        // ==========================================
        console.log('Mengisi rincian spesifikasi teknis alat...');

        // Karena komponen input tidak memiliki atribut name statis, kita ambil seluruh koleksi tag input teks di form
        let inputs = await driver.findElements(By.css('form input[type="text"]'));
        
        // inputs[0] merujuk pada Tipe/Varian (labels.typeLabel)
        await inputs[0].sendKeys('Portable Kit');

        // inputs[1] merujuk pada Ukuran (labels.sizeLabel -> Volume m3)
        await inputs[1].sendKeys('1 m3');

        // inputs[2] merujuk pada Kapasitas/Beban (labels.capLabel -> Tinggi cm)
        await inputs[2].sendKeys('65 cm');

        // Mengisi Jumlah Stok Awal (Berjenis input type="number")
        let stockInput = await driver.findElement(By.css('form input[type="number"]'));
        await stockInput.sendKeys('5');

        // Mengisi Deskripsi Singkat (Textarea)
        let descriptionTextarea = await driver.findElement(By.css('form textarea'));
        await descriptionTextarea.sendKeys('Tabung oksigen lengkap dengan regulator, troli, dan masker siap pakai.');


        // ==========================================
        // LANGKAH 5: SIMULASI UPLOAD FOTO BUKTI ALAT
        // ==========================================
        console.log('Menyuntikkan file gambar alat medis...');
        let toolImagePath = path.join(__dirname, 'test_tool.png');
        let fileInput = await driver.findElement(By.css('form input[type="file"]'));
        await fileInput.sendKeys(toolImagePath);


        // ==========================================
        // LANGKAH 6: SUBMIT DATA FORM INVENTARIS
        // ==========================================
        console.log('Mengklik tombol Simpan Data...');
        // Menargetkan tombol simpan data yang berada di baris footer modal
        let submitButton = await driver.findElement(By.xpath("//button[@type='submit' and contains(., 'Simpan Data')]"));
        await submitButton.click();

        // Jeda penutup untuk memastikan request API dari onSubmit sukses diproses oleh React
        await driver.sleep(2500);
        console.log('✅ TES SELESAI: Penambahan inventaris alat baru berhasil disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat otomasi komponen AddToolModal:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningAddToolTest();