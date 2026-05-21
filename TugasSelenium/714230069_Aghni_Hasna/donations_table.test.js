import { Builder, By, until } from 'selenium-webdriver';

async function runningAdminDonationsTableTest() {
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

        await driver.wait(until.urlContains('admin'), 5000);
        console.log('✅ Login Admin Sukses!');


        // ==========================================
        // LANGKAH 2: MASUK KE TAB DONASI
        // ==========================================
        console.log('Menuju dashboard utama admin...');
        await driver.get('http://localhost:5173/#/admin/dashboard'); 

        console.log('Mencari dan mengklik tab menu Donasi...');
        let donasiTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Donasi (') or contains(text(), 'Donasi')]")), 
            5000
        );
        await donasiTab.click();
        await driver.sleep(1500); // Tunggu data tabel ke-render


        // ==========================================
        // LANGKAH 3: KLIK TOMBOL REVIEW PADA DATA PENDING
        // ==========================================
        console.log('Mencari baris donasi berstatus "Menunggu Review" dan mengklik tombol Review...');
        let reviewButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Review')]")), 
            5000
        );
        await reviewButton.click();
        await driver.sleep(1000); // Tunggu modal terbuka sempurna


        // ==========================================
        // LANGKAH 4: SIMULASI TERIMA BARANG FISIK
        // ==========================================
        console.log('Mendeteksi tombol "Terima Barang (Fisik)"...');
        let receiveButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Terima Barang (Fisik)')]")),
            5000
        );
        await receiveButton.click();
        await driver.sleep(500); // Tunggu modal konfirmasi internal muncul

        console.log('Mengklik "Ya, Konfirmasi" pada modal konfirmasi...');
        let confirmClick = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Ya, Konfirmasi')]")),
            5000
        );
        await confirmClick.click();
        
        // Jeda waktu agar backend memproses perubahan status dari pending -> received
        console.log('Menunggu sistem memperbarui status menjadi received...');
        await driver.sleep(2000);


        // ==========================================
        // LANGKAH 5: PROSES QUALITY CONTROL (QC)
        // ==========================================
        // Karena setelah konfirmasi modal otomatis menutup (berdasarkan fungsi handleCloseModal di kodemu),
        // kita klik ulang baris data yang sekarang statusnya sudah berubah menjadi "Proses QC"
        console.log('Membuka kembali modal donasi yang sudah berstatus Proses QC...');
        let qcButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(., 'Proses QC')]")), 
            5000
        );
        await qcButton.click();
        await driver.sleep(1000);

        console.log('Memilih hasil cek fisik kondisi barang pada dropdown...');
        // Sekarang select pasti ada karena statusnya sudah 'received'
        let conditionSelect = await driver.wait(
            until.elementLocated(By.xpath("//select[option[contains(text(), 'Baik (Layak Pakai)')]]")), 
            5000
        );
        await conditionSelect.sendKeys('Baik (Layak Pakai)');
        await driver.sleep(500);


        // ==========================================
        // LANGKAH 6: VALIDASI AKHIR & MASUK STOK
        // ==========================================
        console.log('Mengklik tombol Validasi QC & Masuk Stok...');
        let validateButton = await driver.findElement(
            By.xpath("//button[contains(., 'Validasi QC & Masuk Stok')]")
        );
        await validateButton.click();

        await driver.sleep(2000); // Tunggu integrasi ke stok selesai
        console.log('✅ TES SELESAI: Seluruh alur review donasi, terima fisik, hingga QC sukses disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat alur peninjauan donasi:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningAdminDonationsTableTest();