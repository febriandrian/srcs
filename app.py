from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Sekolah

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///srcs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'rahasia'

db.init_app(app)
from flask import redirect, url_for

@app.route('/')
def index():
    return redirect(url_for('login'))

# ====================
# CREATE USER DEFAULT
# ====================
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

    db.session.commit()

# ====================
# ROUTE LOGIN
# ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            session['username'] = user.username
            session['role'] = user.role

            # Arahkan berdasarkan role
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

# ====================
# ROUTE PER ROLE
# ====================
@app.route('/safety-riding')
def safety_riding():
    if 'role' not in session or session['role'] != 'PetugasSR':
        return "Akses ditolak"
    return render_template('safety_riding.html')

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

@app.route('/laporan')
def laporan():
    if 'role' not in session or session['role'] != 'Manager':
        return "Akses ditolak"
    return render_template('laporan.html')

# ====================
# RUN SERVER
# ====================
if __name__ == '__main__':
    with app.app_context():
        create_data()
    app.run(debug=True)
