import { Builder, By, until } from 'selenium-webdriver';

async function runningLoanTest() {
    // 1. Membuka browser Chrome
    let driver = await new Builder().forBrowser('chrome').build();

    try {
        // ==========================================
        // LANGKAH 1: LOGIN USER TERVERIFIKASI
        // ==========================================
        console.log('Mengakses halaman login...');
        await driver.get('http://localhost:5173/#/login'); 
        await driver.manage().window().maximize();

        let emailInput = await driver.wait(until.elementLocated(By.css('input[type="email"]')), 5000);
        let passwordInput = await driver.findElement(By.css('input[type="password"]'));
        
        // ⚠️ PENTING: Gunakan akun testing yang data profil KTP-nya sudah LENGKAP & TERVERIFIKASI
        // Supaya form pengajuan pinjaman muncul di layar detail alat.
        await emailInput.sendKeys('aghniihsn@gmail.com');
        await passwordInput.sendKeys('123456');
        await driver.findElement(By.css('button[type="submit"]')).click();

        // Tunggu hingga masuk ke dashboard utama
        await driver.wait(until.urlContains('dashboard'), 5000);
        console.log('✅ Login Sukses!');


        // ==========================================
        // LANGKAH 2: MENUJU HALAMAN DETAIL ALAT (ID ALAT)
        // ==========================================
        // Kita simulasikan langsung menembak ke ID alat contoh yang ada di database kamu (misal ID: 1)
        // Silakan sesuaikan angka '1' di akhir URL dengan ID alat yang berstatus ready di database kamu.
        let targetToolId = "6a0dbfc420cccb5d49cf4cbc"; 
        console.log(`Navigasi ke halaman detail alat dengan ID: ${targetToolId}...`);
        await driver.get(`http://localhost:5173/#/alat/${targetToolId}`); 


        // ==========================================
        // LANGKAH 3: PENGISIAN FORMULIR PINJAM ALAT
        // ==========================================
        console.log('Memeriksa ketersediaan form peminjaman...');
        
        // Memastikan input tanggal mulai pinjam dimuat (Indikator user terverifikasi)
        let loanDateInput = await driver.wait(
            until.elementLocated(By.css('input[name="loanDate"]')), 
            5000
        );

        console.log('Mulai mengisi formulir pengajuan pinjaman...');

        // 1. Mengisi Tanggal Mulai Pinjam (Format: YYYY-MM-DD)
        await loanDateInput.sendKeys('2026-06-01');

        // 2. Mengisi Rencana Tanggal Kembali
        let returnDueInput = await driver.findElement(By.css('input[name="returnDue"]'));
        await returnDueInput.sendKeys('2026-06-15');

        // 3. Mengisi Kondisi Medis Pasien (Ditembak berdasarkan placeholder)
        let conditionInput = await driver.findElement(By.css('input[placeholder="Cth: Patah Tulang, Stroke"]'));
        await conditionInput.sendKeys('Pasien pasca operasi patah tulang kaki kanan');

        // 4. Mengisi Tujuan Penggunaan / Catatan Tambahan (Textarea)
        let notesTextarea = await driver.findElement(By.css('textarea[placeholder="Jelaskan kebutuhan Anda..."]'));
        await notesTextarea.sendKeys('Digunakan untuk membantu mobilisasi latihan berjalan pasien di dalam rumah selama masa pemulihan.');


        // ==========================================
        // LANGKAH 4: MENGIRIM PERMINTAAN (SUBMIT FORM)
        // ==========================================
        console.log('Mengklik tombol Ajukan Permintaan...');
        let submitButton = await driver.findElement(By.css('button[type="submit"]'));
        
        // Memastikan tombol tidak dalam kondisi ter-disabled (karena stok kosong)
        if (await submitButton.isEnabled()) {
            await submitButton.click();

            // Validasi: Berdasarkan kodemu, jika berhasil akan muncul notifikasi sukses
            // dan dialihkan kembali ke '/dashboard' setelah 2 detik
            await driver.wait(until.urlContains('dashboard'), 5000);
            console.log('✅ TES SELESAI: Formulir peminjaman alat berhasil diajukan otomatis!');
        } else {
            console.log('❌ TES GAGAL: Tombol ajukan terkunci. Kemungkinan stok alat habis (stok = 0).');
        }

    } catch (error) {
        console.error('❌ TES GAGAL: Terjadi kesalahan saat memproses pengujian:', error);
    } finally {
        console.log('Menutup browser pengujian...');
        await driver.quit();
    }
}

runningLoanTest();