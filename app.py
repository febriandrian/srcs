from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Sekolah
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///srcs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rahasia'

db.init_app(app)

# ==========================
# REDIRECT BERANDA → LOGIN
# ==========================
@app.route('/')
def index():
    return redirect(url_for('login'))

# ==========================
# BUAT USER DEFAULT & DB
# ==========================
def create_data():
    db.create_all()

    if not User.query.filter_by(username='sr').first():
        db.session.add(User(username='sr', password='123', role='PetugasSR'))
    if not User.query.filter_by(username='hc').first():
        db.session.add(User(username='hc', password='123', role='PetugasHC'))
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password='123', role='Admin'))
    if not User.query.filter_by(username='manager').first():
        db.session.add(User(username='manager', password='123', role='Manager'))

    if not Sekolah.query.first():
        db.session.add(Sekolah(
            nama="SMK N 1 Pontianak",
            kabupaten="Pontianak",
            tanggal_kunjungan=date(2025, 9, 1)
        ))

    db.session.commit()

# ==========================
# ROUTE LOGIN & LOGOUT
# ==========================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['username'] = user.username
            session['role'] = user.role

            if user.role == 'PetugasSR':
                return redirect('/safety-riding')
            elif user.role == 'PetugasHC':
                return redirect('/community')
            elif user.role == 'Admin':
                return redirect('/dashboard')
            elif user.role == 'Manager':
                return redirect('/laporan')
        else:
            return "Login gagal. Cek username/password."

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==========================
# ROUTE SESUAI ROLE
# ==========================
@app.route('/safety-riding')
def safety_riding():
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"
    return render_template('safety_riding.html', role=session['role'])

@app.route('/community')
def community():
    if 'role' not in session or session['role'] != 'PetugasHC':
        return "Akses ditolak"
    return render_template('community.html')

@app.route('/dashboard')
def dashboard():
    if 'role' not in session or session['role'] != 'Admin':
        return "Akses ditolak"
    return render_template('dashboard.html')

# ==========================
# SEKOLAH - LIST & TAMBAH
# ==========================
@app.route('/safety-riding/sekolah/<int:sekolah_id>')
def lihat_sekolah(sekolah_id):
    sekolah = Sekolah.query.get_or_404(sekolah_id)
    return render_template('lihat_sekolah.html', sekolah=sekolah)

@app.route('/safety-riding/sekolah/edit/<int:sekolah_id>', methods=['GET', 'POST'])
def edit_sekolah(sekolah_id):
    sekolah = Sekolah.query.get_or_404(sekolah_id)

    if request.method == 'POST':
        sekolah.nama = request.form['nama']
        sekolah.kabupaten = request.form['kabupaten']
        sekolah.tanggal_kunjungan = datetime.strptime(request.form['tanggal_kunjungan'], '%Y-%m-%d').date()

        db.session.commit()
        return redirect('/safety-riding/sekolah')

    return render_template('edit_sekolah.html', sekolah=sekolah)

@app.route('/safety-riding/sekolah')
def list_sekolah():
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"

    sekolah_list = Sekolah.query.all()
    return render_template('list_sekolah.html', sekolah_list=sekolah_list)
@app.route('/safety-riding/sekolah/hapus/<int:sekolah_id>', methods=['POST'])
def hapus_sekolah(sekolah_id):
    sekolah = Sekolah.query.get_or_404(sekolah_id)
    db.session.delete(sekolah)
    db.session.commit()
    return redirect(url_for('list_sekolah'))




    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"

    sekolah = Sekolah.query.get_or_404(id)
    db.session.delete(sekolah)
    db.session.commit()

    return redirect(url_for('list_sekolah'))

@app.route('/safety-riding/sekolah/tambah', methods=['GET', 'POST'])
def sekolah_tambah():
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"

    if request.method == 'POST':
        nama = request.form['nama']
        kabupaten = request.form['kabupaten']
        tanggal_kunjungan = datetime.strptime(request.form['tanggal_kunjungan'], '%Y-%m-%d').date()

        sekolah_baru = Sekolah(nama=nama, kabupaten=kabupaten, tanggal_kunjungan=tanggal_kunjungan)
        db.session.add(sekolah_baru)
        db.session.commit()
        return redirect('/safety-riding/sekolah')

    return render_template('tambah_sekolah.html')

# ==========================
# LAPORAN MANAGER
# ==========================
@app.route('/laporan')
def laporan():
    if 'role' not in session or session['role'] != 'Manager':
        return "Akses ditolak"
    return render_template('laporan.html')

# ==========================
# JALANKAN SERVER
# ==========================
if __name__ == '__main__':
    with app.app_context():
        create_data()
    app.run(debug=True)
