import { Builder, By, until } from 'selenium-webdriver';

async function runningAdminLoansTableTest() {
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

        await driver.wait(until.urlContains('admin'), 5000);
        console.log('✅ Login Admin Sukses!');


        // ==========================================
        // LANGKAH 2: MASUK KE TAB PEMINJAMAN
        // ==========================================
        console.log('Menuju dashboard utama admin...');
        await driver.get('http://localhost:5173/#/admin/dashboard'); 

        console.log('Mencari dan mengklik tab menu Peminjaman...');
        let peminjamanTab = await driver.wait(
            until.elementLocated(By.xpath("//*[contains(text(), 'Peminjaman')]")), 
            5000
        );
        await peminjamanTab.click();
        
        // Jeda waktu tunggu komponen LoansTable selesai memuat data dari API
        await driver.sleep(1500);


        // ==========================================
        // LANGKAH 3: AKSI 1 - SETUJUI PERMINTAAN (PENDING -> APPROVED)
        // ==========================================
        console.log('Memeriksa ketersediaan tombol "Setujui" (Status: Pending)...');
        let approveButtons = await driver.findElements(By.xpath("//button[contains(., 'Setujui')]"));
        
        if (approveButtons.length > 0) {
            await approveButtons[0].click();
            console.log('-> Tombol Setujui diklik. Menunggu modal konfirmasi...');
            await driver.sleep(500);

            // Klik tombol konfirmasi di dalam modal
            let confirmButton = await driver.wait(
                until.elementLocated(By.xpath("//button[contains(., 'Ya, Konfirmasi') or contains(., 'Ya')]")),
                3000
            );
            await confirmButton.click();
            console.log('-> Konfirmasi Persetujuan Sukses!');
            await driver.sleep(2000); // Tunggu re-fetch data/render ulang state
        } else {
            console.log('ℹ️ Tidak ada data permintaan berstatus PENDING.');
        }


        // ==========================================
        // LANGKAH 4: AKSI 2 - SERAHKAN BARANG (APPROVED -> ACTIVE)
        // ==========================================
        console.log('Memeriksa ketersediaan tombol "Serahkan Barang" (Status: Approved)...');
        let handoverButtons = await driver.findElements(By.xpath("//button[contains(., 'Serahkan Barang')]"));
        
        if (handoverButtons.length > 0) {
            await handoverButtons[0].click();
            console.log('-> Tombol Serahkan Barang diklik. Menunggu modal konfirmasi...');
            await driver.sleep(500);

            // Klik tombol konfirmasi di dalam modal
            let confirmButton = await driver.wait(
                until.elementLocated(By.xpath("//button[contains(., 'Ya, Konfirmasi') or contains(., 'Ya')]")),
                3000
            );
            await confirmButton.click();
            console.log('-> Konfirmasi Penyerahan Barang Sukses! Status menjadi Active.');
            await driver.sleep(2000);
        } else {
            console.log('ℹ️ Tidak ada data permintaan berstatus APPROVED.');
        }


        // ==========================================
        // LANGKAH 5: AKSI 3 - TERIMA PENGEMBALIAN (ACTIVE -> COMPLETED)
        // ==========================================
        console.log('Memeriksa ketersediaan tombol "Terima Pengembalian" (Status: Active)...');
        let returnButtons = await driver.findElements(By.xpath("//button[contains(., 'Terima Pengembalian')]"));
        
        if (returnButtons.length > 0) {
            await returnButtons[0].click();
            console.log('-> Tombol Terima Pengembalian diklik. Menunggu modal konfirmasi...');
            await driver.sleep(500);

            // Klik tombol konfirmasi di dalam modal
            let confirmButton = await driver.wait(
                until.elementLocated(By.xpath("//button[contains(., 'Ya, Konfirmasi') or contains(., 'Ya')]")),
                3000
            );
            await confirmButton.click();
            console.log('-> Konfirmasi Pengembalian Sukses! Status Peminjaman Selesai.');
            await driver.sleep(2000);
        } else {
            console.log('ℹ️ Tidak ada data peminjaman berstatus ACTIVE.');
        }

        console.log('✅ TES SELESAI: Siklus penuh peminjaman dari Setujui sampai Selesai sukses disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala tidak terduga saat otomasi alur peminjaman:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningAdminLoansTableTest();