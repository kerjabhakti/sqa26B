import { Builder, By, until } from 'selenium-webdriver';
import path from 'path';
import { fileURLToPath } from 'url';

// Konfigurasi untuk mendapatkan jalur folder saat ini (Wajib untuk ES Modules)
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runningProfileTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // ==========================================
        // LANGKAH 1: LOGIN KE SISTEM MEDISLINK
        // ==========================================
        console.log('Mengakses halaman login...');
        await driver.get('http://localhost:5173/#/login'); 
        await driver.manage().window().maximize();

        let emailInput = await driver.wait(until.elementLocated(By.css('input[type="email"]')), 5000);
        let passwordInput = await driver.findElement(By.css('input[type="password"]'));
        
        // Sesuai akun testing milikmu
        await emailInput.sendKeys('aghniihsn@gmail.com');
        await passwordInput.sendKeys('123456');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu hingga masuk ke dashboard
        await driver.wait(until.urlContains('dashboard'), 5000);
        console.log('✅ Login Sukses!');


        // ==========================================
        // LANGKAH 2: NAVIGASI KE HALAMAN PROFIL
        // ==========================================
        console.log('Navigasi langsung ke route halaman profil...');
        await driver.get('http://localhost:5173/#/profile'); 

        // Tunggu hingga tombol "Lengkapi Data Diri" muncul di layar
        let editModeButton = await driver.wait(
            until.elementLocated(By.xpath("//button[contains(text(), 'Lengkapi Data Diri')]")), 
            5000
        );
        
        console.log('Mengklik tombol Lengkapi Data Diri untuk membuka Form Edit...');
        await editModeButton.click();
        await driver.sleep(500); // Jeda animasi transisi form


        // ==========================================
        // LANGKAH 3: SIMULASI UPLOAD FOTO PROFIL
        // ==========================================
        console.log('Mengunggah foto profil baru...');
        let profileImagePath = path.join(__dirname, 'test_profile.png');
        // Mencari input file pertama (ganti foto profil)
        let profileFileInput = await driver.findElement(By.css('input[type="file"]'));
        await profileFileInput.sendKeys(profileImagePath);


        // ==========================================
        // LANGKAH 4: MENGISI FORM INPUT TEXT
        // ==========================================
        console.log('Mengisi data text (Nama, WA, Alamat, NIK)...');

        // 1. Mengisi Nama Lengkap (Ditembak berdasarkan placeholder)
        let nameInput = await driver.findElement(By.css('input[placeholder="Nama Sesuai KTP"]'));
        await nameInput.clear();
        await nameInput.sendKeys('Aghniihsn Ahmad');

        // 2. Mengisi No. WhatsApp
        let phoneInput = await driver.findElement(By.css('input[placeholder="08..."]'));
        await phoneInput.clear();
        await phoneInput.sendKeys('081234567890');

        // 3. Mengisi Alamat Domisili (Textarea)
        let addressInput = await driver.findElement(By.css('textarea[placeholder="Alamat lengkap..."]'));
        await addressInput.clear();
        await addressInput.sendKeys('Kompleks ULBI Blok C No. 12, Cimahi, Jawa Barat');

        // 4. Mengisi NIK 16 Digit
        let nikInput = await driver.findElement(By.css('input[placeholder="NIK"]'));
        // Jika akun sudah terverifikasi sebelumnya, NIK akan disabled. Kita cek dulu kondisinya.
        if (await nikInput.isEnabled()) {
            await nikInput.clear();
            await nikInput.sendKeys('3273012345670001');
        } else {
            console.log('ℹ️ Input NIK terkunci (sudah pernah diverifikasi sebelumnya).');
        }


        // ==========================================
        // LANGKAH 5: SIMULASI UPLOAD FOTO KTP
        // ==========================================
        // Kita cari input file yang berada di dalam section KTP (card orange)
        // Jika akun belum pernah upload KTP, elemen input ini akan aktif
        try {
            let ktpFileInput = await driver.findElement(By.css('.bg-orange-50 input[type="file"]'));
            if (await ktpFileInput.isEnabled()) {
                console.log('Mengunggah foto KTP baru...');
                let ktpImagePath = path.join(__dirname, 'test_ktp.jpg');
                await ktpFileInput.sendKeys(ktpImagePath);
            }
        } catch (error) {
            console.log('ℹ️ Form upload KTP tidak mendeteksi input kosong (KTP sudah terpasang).');
            console.log(error)
        }


        // ==========================================
        // LANGKAH 6: SIMPAN DATA PROFIL
        // ==========================================
        console.log('Mengklik tombol Simpan Data...');
        let saveButton = await driver.findElement(By.xpath("//button[contains(., 'Simpan Data')]"));
        await saveButton.click();

        // Validasi: Menunggu notifikasi sukses muncul di layar
        let successAlert = await driver.wait(
            until.elementLocated(By.className('bg-teal-600')), 
            5000
        );
        console.log(`🎉 Notifikasi sistem: "${await successAlert.getText()}"`);
        
        console.log('✅ TES SELESAI: Pembaruan data profil MedisLink berhasil disimulasikan!');

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kendala saat otomasi profil:', error);
    } finally {
        console.log('Menutup browser...');
        await driver.quit();
    }
}

runningProfileTest();