from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'
db = SQLAlchemy(app)

# Tabela w bazie danych na maile
class Subscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Automatyczne tworzenie bazy
with app.app_context():
    db.create_all()

# Twoje filmy
movies = [
    {"title": "Incepcja", "rating": 5, "review": "Sen wewnątrz snu.", "img": "/static/inception.jpg"},
    {"title": "Diuna 2", "rating": 5, "review": "Wizualne arcydzieło.", "img": "/static/dune2.jpg"},
    {"title": "Batman", "rating": 4, "review": "Mroczny klimat.", "img": "/static/batman.jpg"}
]

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    if email:
        try:
            new_sub = Subscriber(email=email)
            db.session.add(new_sub)
            db.session.commit()
            return "<h1>Sukces! Zostałeś zapisany do newslettera.</h1><a href='/'>Wróć</a>"
        except:
            return "<h1>Ten e-mail już jest w bazie!</h1><a href='/'>Wróć</a>"
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)