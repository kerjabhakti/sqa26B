import { Builder, By, Key, until } from 'selenium-webdriver';

async function runningMedisLinkTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // 2. Buka URL MedisLink yang sedang jalan di localhost kamu
        await driver.get('http://localhost:5173/#/login'); 

        // 3. Maksimalkan ukuran browser
        await driver.manage().window().maximize();

        // 4. Cari input Email berdasarkan CSS Selector (Mencari tag input yang memiliki type="email")
        let emailInput = await driver.wait(
            until.elementLocated(By.css('input[type="email"]')), 
            5000
        );
        
        // 5. Cari input Password berdasarkan CSS Selector (Mencari tag input yang memiliki type="password")
        let passwordInput = await driver.findElement(By.css('input[type="password"]'));

        // 6. Simulasikan mengetik akun data user (Gunakan akun dummy/test yang terdaftar di database kamu)
        await emailInput.sendKeys('aghniihsn@gmail.com');
        await passwordInput.sendKeys('123456');

        // 7. Cari tombol submit/login berdasarkan tipe submit
        let loginButton = await driver.findElement(By.css('button[type="submit"]'));
        
        // 8. Klik tombol login
        await loginButton.click();

        // 9. Validasi Pengujian:
        // Karena sistem kamu membagi dashboard berdasarkan role (bisa ke '/admin/dashboard' atau ke '/dashboard'),
        // kita tunggu sampai URL-nya mengandung kata 'dashboard'.
        await driver.wait(until.urlContains('dashboard'), 5000);
        
        console.log('✅ TES SELESAI: Alur login MedisLink berhasil disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kesalahan saat pengujian:', error);
    } finally {
        // Menutup browser otomatis setelah selesai pengujian
        await driver.quit();
    }
}

runningMedisLinkTest();