import { Builder, By, until } from 'selenium-webdriver';

async function runningRegisterTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        console.log('Mengakses halaman registrasi MedisLink...');
        // 2. Buka URL Register menggunakan Hash Router aplikasimu
        await driver.get('http://localhost:5173/#/register'); 
        await driver.manage().window().maximize();

        // ==========================================
        // LANGKAH 1: PENGISIAN FORM REGISTRASI
        // ==========================================
        console.log('Mulai mengisi form data registrasi...');

        // 1. Mengisi Nama Lengkap (Berdasarkan placeholder)
        let nameInput = await driver.wait(
            until.elementLocated(By.css('input[placeholder="Nama Lengkap"]')), 
            5000
        );
        await nameInput.sendKeys('Aghniihsn Tester');

        // 2. Mengisi Email (Berdasarkan placeholder)
        let emailInput = await driver.findElement(By.css('input[placeholder="Email"]'));
        // Gunakan email dinamis/acak agar tidak error "Email sudah terdaftar" saat tes dijalankan ulang
        let randomEmail = `tester.${Math.floor(Math.random() * 10000)}@gmail.com`;
        await emailInput.sendKeys(randomEmail);
        console.log(`Email pendaftaran dinamis yang digunakan: ${randomEmail}`);

        // 3. Mengisi Nomor Telepon (Berdasarkan placeholder atau type="number")
        let phoneInput = await driver.findElement(By.css('input[type="number"]'));
        await phoneInput.sendKeys('085123456789');

        // 4. Mengisi Password (Berdasarkan placeholder)
        let passwordInput = await driver.findElement(By.css('input[placeholder="Password"]'));
        await passwordInput.sendKeys('AmanBanget123');

        // 5. Mengisi Konfirmasi Password (Berdasarkan placeholder)
        let confirmPasswordInput = await driver.findElement(By.css('input[placeholder="Konfirmasi Password"]'));
        await confirmPasswordInput.sendKeys('AmanBanget123');


        // ==========================================
        // LANGKAH 2: SUBMIT DATA FORM
        // ==========================================
        console.log('Mengklik tombol Daftar...');
        let registerButton = await driver.findElement(By.css('button[type="submit"]'));
        await registerButton.click();


        // ==========================================
        // LANGKAH 3: VALIDASI BERHASIL REGISTRASI
        // ==========================================
        console.log('Menunggu respons validasi sistem...');
        
        // Memastikan box notifikasi sukses (berwarna hijau/bg-green-100) muncul di layar
        let successAlert = await driver.wait(
            until.elementLocated(By.className('bg-green-100')), 
            5000
        );
        console.log(`🎉 Notifikasi Sistem: "${await successAlert.getText()}"`);

        // Sesuai dengan setTimeout di kodemu (2000ms), halaman akan otomatis pindah ke '/login'
        console.log('Menunggu pengalihan otomatis ke halaman login...');
        await driver.wait(until.urlContains('login'), 5000);
        
        console.log('✅ TES SELESAI: Alur registrasi user baru berhasil disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat proses otomasi registrasi:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningRegisterTest();