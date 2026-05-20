import { Builder, By, until } from 'selenium-webdriver';

async function runningEditToolTest() {
    // 1. Inisialisasi Driver Browser Chrome
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
        // LANGKAH 2: MASUK KE TAB INVENTARIS & KLIK EDIT ALAT
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

        console.log('Mencari tombol Edit pada salah satu data alat...');
        // Mensimulasikan klik tombol aksi edit (ikon pensil/tombol berteks Edit) pada list alat pertama
        let editActionButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Edit') or @title='Edit']")), 
            5000
        );
        await editActionButton.click();


        // ==========================================
        // LANGKAH 3: MERUBAH DATA INFORMASI DASAR MODAL
        // ==========================================
        console.log('Form modal terbuka. Melakukan pembaruan informasi dasar...');
        
        // 1. Mengubah Nama Alat (Menggunakan pencarian placeholder)
        let nameInput = await driver.wait(
            until.elementLocated(By.css('form input[placeholder="Contoh: Kursi Roda"]')), 
            5000
        );
        await nameInput.clear(); // Hapus nilai lama
        await nameInput.sendKeys('Kursi Roda Standard Premium');

        // 2. Mengubah Kategori Alat (Dropdown kategori)
        let categorySelect = await driver.findElement(By.css('form select'));
        await categorySelect.sendKeys('MOBILITAS');


        // ==========================================
        // LANGKAH 4: MERUBAH SPESIFIKASI TEKNIS & STOK
        // ==========================================
        console.log('Melakukan pembaruan rincian spesifikasi teknis...');

        // Menembak sisa input text berdasarkan teks placeholdernya masing-masing
        let typeInput = await driver.findElement(By.css('form input[placeholder="Contoh: Standard, Travel, dll"]'));
        await typeInput.clear();
        await typeInput.sendKeys('Standard Ergo');

        let sizeInput = await driver.findElement(By.css('form input[placeholder="Contoh: 18 inch, M/L/XL"]'));
        await sizeInput.clear();
        await sizeInput.sendKeys('20 inch');

        let weightInput = await driver.findElement(By.css('form input[placeholder="Contoh: 120 kg, 150 cm"]'));
        await weightInput.clear();
        await weightInput.sendKeys('130 kg');

        // Mengubah nilai Stok Tersedia (Input type number tunggal)
        let stockInput = await driver.findElement(By.css('form input[type="number"]'));
        await stockInput.clear();
        await stockInput.sendKeys('12');

        // Mengubah Deskripsi / Keterangan tambahan
        let descriptionTextarea = await driver.findElement(By.css('form textarea'));
        await descriptionTextarea.clear();
        await descriptionTextarea.sendKeys('Kondisi unit cadangan diperbarui dengan bantalan jok yang jauh lebih empuk dan tahan air.');


        // ==========================================
        // LANGKAH 5: MERUBAH STATUS & KONDISI (DROPDOWN BAWAH)
        // ==========================================
        console.log('Menyesuaikan status ketersediaan barang inventaris...');
        
        // Mengambil semua tag select di dalam form, select indeks ke-1 dan ke-2 adalah Kondisi dan Status
        let selects = await driver.findElements(By.css('form select'));
        
        // Mengubah dropdown Kondisi Alat menjadi 'baru'
        await selects[1].sendKeys('baru');
        
        // Mengubah dropdown Status Ketersediaan menjadi 'tersedia'
        await selects[2].sendKeys('tersedia');


        // ==========================================
        // LANGKAH 6: SIMPAN PERUBAHAN DATA FORM EDIT
        // ==========================================
        console.log('Mengklik tombol Simpan Perubahan...');
        let saveButton = await driver.findElement(By.xpath("//button[@type='submit' and contains(., 'Simpan Perubahan')]"));
        await saveButton.click();

        // Berikan durasi jeda waktu tunggu pemrosesan API put/patch oleh backend MedisLink selesai
        await driver.sleep(2500);
        console.log('✅ TES SELESAI: Simulasi pembaruan data EditToolModal berhasil dieksekusi tanpa error!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat proses pengujian form edit alat:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningEditToolTest();