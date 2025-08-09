from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================
# TABEL USER (Untuk Login)
# ============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # PetugasSR, PetugasHC, Admin, Manager

# ============================
# TABEL SEKOLAH (Safety Riding)
# ============================
class Sekolah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kabupaten = db.Column(db.String(100), nullable=False)
    tanggal_kunjungan = db.Column(db.Date, nullable=False)

# ============================
# TABEL PESERTA (Absensi)
# ============================
class Peserta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(50))
    jenis_motor = db.Column(db.String(100))
    no_hp = db.Column(db.String(30))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sekolah_id = db.Column(db.Integer, db.ForeignKey('sekolah.id'), nullable=False)
    sekolah = db.relationship('Sekolah', backref=db.backref('peserta_list', lazy=True))

# ============================
# TABEL MOTOR DI PARKIRAN (rekap per merek & model)
# ============================
class MotorParkir(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    sekolah_id = db.Column(db.Integer, db.ForeignKey('sekolah.id'), nullable=False)
    merek = db.Column(db.String(20), nullable=False)         # Honda | Yamaha | Suzuki | Vespa
    model = db.Column(db.String(100), nullable=False)        # misal: Vario 160, NMAX, Satria F150, Primavera
    jumlah = db.Column(db.Integer, nullable=False, default=1)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sekolah = db.relationship('Sekolah', backref=db.backref('motor_list', lazy=True))
