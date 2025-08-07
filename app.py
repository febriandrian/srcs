from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///srcs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Buat route utama
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Inisialisasi database sebelum app jalan
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
