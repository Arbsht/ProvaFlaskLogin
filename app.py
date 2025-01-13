from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = 'key_sessione_user' #chiave per la sessione user
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#inizializza db e flask-login
db.init_app(app)
login_manager = LoginManager() #inizializza flask-login
login_manager.init_app(app) #collega flask-login e flask
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()
#implementazione route e metodi#

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        #check se l'utente esiste nel db
        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Questo username è già in uso.")
        if len(username) < 3 and len(password) < 7:
            return render_template('register.html', error="Lo username e la password usati sono troppo corti (min 4 per username, min 8 per password)")
        if len(username) < 3:
            return render_template('register.html', error="Lo username usato è troppo corto (minimo 4 caratteri)")
        if len(password) < 7:
            return render_template('register.html', error="La password usata è troppo corta (minimo 8 caratteri)")
        #crea user e lo salva nel db
        pw_hash = bcrypt.generate_password_hash(password, 10)
        new_user = User(username=username, password=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', error=None)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] #prende dati dalle form
        password = request.form['password']
        #cerca user db
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password): #se user esiste
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error="Credenziali non valide.") #errore se credenziali errate
    return render_template('login.html', error=None)

@app.route('/home')
@login_required #solo se user è autenticato
def home():
    return render_template('home.html', username=current_user.username)

@app.route('/logout')
@login_required
def logout():
    logout_user() #logout user
    return redirect(url_for('login')) #torniamo al login

if __name__ == '__main__': #debug
    app.run(debug=True)