# 🐞 Bug Log Summary: AerialCast E2E Testing

**Date:** 2026-05-21 | **Target:** Next.js 16 (FE) & Flask (BE)
**Status Keseluruhan:** 🔴 **24 dari 27 Test GAGAL (Blocked)** | ✅ **3 Test Lulus**

---

## 🚨 Critical Blockers (Segera Perbaiki)

**1. Server 500 Error pada Autentikasi (Auth Flow)**
* **Dampak:** Memblokir 24 *test case* yang butuh sesi login.
* **Penyebab:** Database *staging* Neon PostgreSQL mengalami kelelahan koneksi (*connection pool exhausted*) karena sering di-hit selama *testing*, memicu *error* 500 saat registrasi *user*.
* **Solusi:** * Pindah ke **PostgreSQL/TimescaleDB lokal via Docker** khusus buat *testing*.
    * Tambahkan *connection pooling* di Flask (pakai `pgbouncer` atau SQLAlchemy `pool_pre_ping=True`).
    * Tambahkan *retry logic* di file `conftest.py`.

**2. Cleanup Fixture Menghapus Session Test User**
* **Dampak:** *Test user* terhapus setelah tes pertama jalan, bikin tes berikutnya gagal login.
* **Status:** Sebagian sudah di-komen di `db_helpers.py`, tapi DB masih tidak stabil karena sisa koneksi sebelumnya.

---

## ⚠️ Functional & Test Design Issues (Prioritas Menengah)

**1. Telemetry Gagal karena Syarat Flight Chain**
* **Kendala:** Backend menolak data telemetri tiruan karena sistem butuh rantai status yang lengkap: `Drone (READY) -> Mission (APPROVED) -> Session (LIVE)`.
* **Solusi:** Buat fungsi *helper* `_setup_flight_session()` di Python untuk merekayasa seluruh rantai status ini sebelum Selenium mulai ngetes UI Telemetry.

**2. MQTT Listener Spamming Console**
* **Kendala:** Output console dipenuhi pesan log *"Telemetry ignored"* dari `mqtt_listener.py` saat skrip tiruan jalan.
* **Solusi:** Pisahkan topik khusus *testing* (`aerialcast/test/telemetry`) atau tambahkan flag `--quiet` pas mode *testing*.

---

## ✅ Resolved Issues (Sudah Diperbaiki)
* **API URL Mismatch:** *Endpoint* yang salah di tes (misal `/api/drones/`) sudah diganti jadi pakai *prefix* yang benar (`/api/v1/drones/`).
* **UI Selectors DOM:** *Selector* Selenium yang *out-of-sync* dengan elemen Tailwind di Next.js sudah disesuaikan pakai `id` dan pengecekan konten (*fallback*).
* **Admin-Only UI:** Kasus tombol "Add Drone" yang tidak muncul untuk *user* biasa sudah dimitigasi dengan `pytest.skip` untuk *role non-admin*.
* **Console Error False Positive:** Validasi *error* palsu dari *tag script* bawaan *build* Next.js sudah diatasi pakai *visibility timeout*.

---

## 🛠️ Action Plan Selanjutnya
1. **[P0]** Bikin database *testing* di Docker lokal untuk menghindari *rate-limit* dari Neon.
2. **[P0]** Inisiasi pembuatan *test user* secara manual/statis di API tanpa perlu registrasi berulang di setiap *session*.
3. **[P1]** Implementasi *helper function* buat *mocking* status misi dan penerbangan.
