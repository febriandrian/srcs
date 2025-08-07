from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Tabel User (login)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # PetugasSR, PetugasHC, Admin, Manager

# Tabel Sekolah (Safety Riding)
class Sekolah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    alamat = db.Column(db.String(200), nullable=False)
    tanggal_kunjungan = db.Column(db.Date, nullable=False)
