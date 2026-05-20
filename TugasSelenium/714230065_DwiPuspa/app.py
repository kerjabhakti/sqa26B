from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Konfigurasi Database
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="",
    database="library_db"
)

# Route untuk Form HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk Tambah Data Buku
@app.route('/add', methods=['POST'])
def add_book():
    data = request.form
    judul = data['judul']
    penulis = data['penulis']
    tahun_terbit = data['tahun_terbit']

    # Validasi Data
    errors = []

    # Validasi judul tidak boleh kosong
    if not judul.strip():
        errors.append("Judul tidak boleh kosong.")

    # Validasi tahun terbit harus valid
    if not tahun_terbit.isdigit() or int(tahun_terbit) < 1900 or int(tahun_terbit) > 2025:
        errors.append("Tahun terbit harus antara 1900 dan 2025.")

    # Jika ada error, kembalikan pesan kesalahan
    if errors:
        return jsonify({"status": "error", "errors": errors}), 400

    # Jika validasi lolos, simpan data ke database
    cursor = db.cursor()
    query = "INSERT INTO books (judul, penulis, tahun_terbit) VALUES (%s, %s, %s)"
    cursor.execute(query, (judul, penulis, tahun_terbit))
    db.commit()
    cursor.close()

    return jsonify({"status": "success", "message": "Buku berhasil ditambahkan!"})

if __name__ == '__main__':
    app.run(debug=True)
