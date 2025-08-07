from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ============================
# TABEL USER (Untuk Login)
# ============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # Contoh isi role: 'PetugasSR', 'PetugasHC', 'Admin', 'Manager'

# ============================
# TABEL SEKOLAH (Safety Riding)
# ============================
class Sekolah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kabupaten = db.Column(db.String(100), nullable=False)  # ganti dari 'alamat'
    tanggal_kunjungan = db.Column(db.Date, nullable=False)

