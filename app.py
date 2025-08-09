from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime, date
from models import db, User, Sekolah, Peserta, MotorParkir

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///srcs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rahasia'

db.init_app(app)

# ======================================================================
# Daftar model (absen peserta: HONDA saja). Parkir: semua merek & model.
# ======================================================================
HONDA_MODELS = [
    "BeAT", "BeAT Street", "Genio", "Scoopy",
    "Vario 125", "Vario 160", "PCX 160", "ADV 160",
    "Revo", "Supra X 125", "Supra GTR 150", "CT125",
    "CB150 Verza", "CB150R Streetfire", "CBR150R", "CBR250RR",
    "CRF150L", "CRF250L", "CRF250 Rally", "EM1 e:"
]
YAMAHA_MODELS = [
    "Mio", "Gear 125", "Fazzio", "FreeGo", "Aerox 155", "NMAX", "Lexi", "Grand Filano",
    "XSR 155", "Vixion", "YZF-R15", "YZF-R25", "MT-15", "WR 155R"
]
SUZUKI_MODELS = ["Nex II", "Address", "Avenis", "Satria F150", "GSX-R150", "GSX-S150"]
VESPA_MODELS  = ["Primavera", "Sprint", "GTS", "Sei Giorni", "LX"]

BRAND_MODELS = {
    "Honda": HONDA_MODELS,
    "Yamaha": YAMAHA_MODELS,
    "Suzuki": SUZUKI_MODELS,
    "Vespa":  VESPA_MODELS,
}
ALLOWED_BRANDS = set(BRAND_MODELS.keys())

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

# ==========================================================
# SAFETY RIDING: HALAMAN LANGSUNG INPUT PARKIR (PETUGAS SR)
# ==========================================================
@app.route('/safety-riding', methods=['GET', 'POST'])
def safety_riding():
    if 'role' not in session or session['role'] != 'PetugasSR':
        return "Akses ditolak"

    sekolah_list = Sekolah.query.order_by(Sekolah.nama.asc()).all()

    if request.method == 'POST':
        sekolah_id = request.form.get('sekolah_id')
        if not sekolah_id:
            return render_template(
                'safety_riding.html',
                sekolah_list=sekolah_list,
                brand_models=BRAND_MODELS,
                brands=list(BRAND_MODELS.keys()),
                msg="Pilih sekolah dulu."
            )

        total_disimpan = 0

        # Baca semua kolom jumlah: <brand_lower>_<index>
        for brand, models in BRAND_MODELS.items():
            slug = brand.lower()  # 'Honda' -> 'honda'
            for i, model in enumerate(models):
                raw = request.form.get(f'{slug}_{i}', '').strip()
                if not raw:
                    continue
                try:
                    jumlah = int(raw)
                except ValueError:
                    jumlah = 0
                if jumlah > 0:
                    db.session.add(MotorParkir(
                        sekolah_id=int(sekolah_id),
                        merek=brand,
                        model=model,
                        jumlah=jumlah
                    ))
                    total_disimpan += jumlah

        if total_disimpan == 0:
            return render_template(
                'safety_riding.html',
                sekolah_list=sekolah_list,
                brand_models=BRAND_MODELS,
                brands=list(BRAND_MODELS.keys()),
                msg="Belum ada jumlah yang diisi (semua kosong/0)."
            )

        db.session.commit()
        return redirect(url_for('lihat_sekolah', sekolah_id=sekolah_id))

    # GET
    return render_template(
        'safety_riding.html',
        sekolah_list=sekolah_list,
        brand_models=BRAND_MODELS,
        brands=list(BRAND_MODELS.keys())
    )

# ==========================
# COMMUNITY & DASHBOARD
# ==========================
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

# ==========================================
# SEKOLAH - LIST / LIHAT / TAMBAH / EDIT / HAPUS
# ==========================================
@app.route('/safety-riding/sekolah')
def list_sekolah():
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"
    sekolah_list = Sekolah.query.all()
    return render_template('list_sekolah.html', sekolah_list=sekolah_list)

@app.route('/safety-riding/sekolah/<int:sekolah_id>')
def lihat_sekolah(sekolah_id):
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin', 'Manager']:
        return "Akses ditolak"
    sekolah = Sekolah.query.get_or_404(sekolah_id)

    peserta = (Peserta.query
               .filter_by(sekolah_id=sekolah.id)
               .order_by(Peserta.created_at.desc())
               .all())

    # Rekap parkir: Brand → {Model → Total}, dan total per Brand
    entries = (MotorParkir.query
               .filter_by(sekolah_id=sekolah.id)
               .order_by(MotorParkir.created_at.desc())
               .all())

    rekap = {}
    brand_totals = {}
    for e in entries:
        rekap.setdefault(e.merek, {})
        rekap[e.merek][e.model] = rekap[e.merek].get(e.model, 0) + e.jumlah
        brand_totals[e.merek] = brand_totals.get(e.merek, 0) + e.jumlah

    form_url = url_for('absen_peserta', sekolah_id=sekolah.id, _external=True)
    return render_template(
        'lihat_sekolah.html',
        sekolah=sekolah,
        peserta=peserta,
        rekap=rekap,
        brand_totals=brand_totals,
        form_url=form_url,
        role=session.get('role')
    )

@app.route('/safety-riding/sekolah/tambah', methods=['GET', 'POST'])
def sekolah_tambah():
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"
    if request.method == 'POST':
        nama = request.form['nama']
        kabupaten = request.form['kabupaten']
        tanggal_kunjungan = datetime.strptime(request.form['tanggal_kunjungan'], '%Y-%m-%d').date()
        db.session.add(Sekolah(nama=nama, kabupaten=kabupaten, tanggal_kunjungan=tanggal_kunjungan))
        db.session.commit()
        return redirect('/safety-riding/sekolah')
    return render_template('tambah_sekolah.html')

@app.route('/safety-riding/sekolah/edit/<int:sekolah_id>', methods=['GET', 'POST'])
def edit_sekolah(sekolah_id):
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"
    sekolah = Sekolah.query.get_or_404(sekolah_id)
    if request.method == 'POST':
        sekolah.nama = request.form['nama']
        sekolah.kabupaten = request.form['kabupaten']
        sekolah.tanggal_kunjungan = datetime.strptime(request.form['tanggal_kunjungan'], '%Y-%m-%d').date()
        db.session.commit()
        return redirect('/safety-riding/sekolah')
    return render_template('edit_sekolah.html', sekolah=sekolah)

@app.route('/safety-riding/sekolah/hapus/<int:sekolah_id>', methods=['POST'])
def hapus_sekolah(sekolah_id):
    if 'role' not in session or session['role'] not in ['PetugasSR', 'Admin']:
        return "Akses ditolak"
    sekolah = Sekolah.query.get_or_404(sekolah_id)
    db.session.delete(sekolah)
    db.session.commit()
    return redirect(url_for('list_sekolah'))

# ==========================
# ABSENSI PESERTA (LINK/QR)
# ==========================
@app.route('/absen/sekolah/<int:sekolah_id>', methods=['GET', 'POST'])
def absen_peserta(sekolah_id):
    sekolah = Sekolah.query.get_or_404(sekolah_id)
    if request.method == 'POST':
        p = Peserta(
            nama=request.form['nama'],
            kelas=request.form.get('kelas'),
            jenis_motor=request.form.get('jenis_motor'),
            no_hp=request.form.get('no_hp'),
            sekolah_id=sekolah.id
        )
        db.session.add(p)
        db.session.commit()
        return render_template('absen_sukses.html', sekolah=sekolah, peserta=p)
    return render_template('form_absen.html', sekolah=sekolah)

# ==========================
# PARKIR (via halaman khusus; tetap dibiarkan)
# ==========================
@app.route('/safety-riding/sekolah/<int:sekolah_id>/parkir/tambah', methods=['GET', 'POST'])
def parkir_tambah(sekolah_id):
    if 'role' not in session or session['role'] != 'PetugasSR':
        return "Akses ditolak"
    sekolah = Sekolah.query.get_or_404(sekolah_id)

    if request.method == 'POST':
        merek = request.form.get('merek')
        model = request.form.get('model')
        try:
            jumlah = int(request.form.get('jumlah', 0))
        except ValueError:
            jumlah = 0

        if merek not in ALLOWED_BRANDS:
            return "Merek tidak valid"
        if model not in BRAND_MODELS[merek]:
            return "Model tidak valid untuk merek ini"
        if jumlah < 1:
            return "Jumlah minimal 1"

        db.session.add(MotorParkir(sekolah_id=sekolah.id, merek=merek, model=model, jumlah=jumlah))
        db.session.commit()
        return redirect(url_for('lihat_sekolah', sekolah_id=sekolah.id))

    return render_template(
        'parkir_tambah.html',
        sekolah=sekolah,
        brand_models=BRAND_MODELS,
        brands=list(BRAND_MODELS.keys())
    )

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
