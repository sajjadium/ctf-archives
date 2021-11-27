from flask import Flask, request, session, redirect, url_for, flash, abort, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import ed25519
import traceback
import os
import re
import sys

app = Flask(__name__)

with open('/secret', 'rb') as f:
    app.secret_key = f.read(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:cybercyber@front-database/front'
app.config['SESSION_COOKIE_NAME'] = 'front'
db = SQLAlchemy(app)

verify_key = ed25519.VerifyingKey(b'~h\x967\xec~\x7f\xa2\xe70\xd2\x05ozg,\xbc\xe9\x15\x98\xdc\x82 \xae;\xbcV\x97\x85%XK')

### Models ###

class User(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.BigInteger, nullable=False)
    nonce = db.Column(db.BigInteger, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.balance = 0
        self.nonce = 0

db.create_all()

### Endpoints ###

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            abort(403)
    return wrap

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect('home')

    return render_template('index.html', login=url_for('login'), register=url_for('register'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    user = User.query.filter_by(name=request.form.get('name', '')).first()

    if not user:
        return "Invalid username", 404

    if not check_password_hash(user.password, request.form.get('passwd', '')):
        return "Invalid password", 403

    session['name'] = user.name
    session['logged_in'] = True

    return redirect('home')


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get('name', '')
    passwd = request.form.get('passwd', '')

    if not (name and passwd):
        abort(400)

    if not re.match("^[a-zA-Z0-9]+$", name):
        return "The username should be alphanumeric", 400

    try:
        user = User(name, generate_password_hash(passwd))
        db.session.add(user)
        db.session.commit()
    except:
        traceback.print_exc()
        return "Username already taken", 400

    session['name'] = user.name
    session['logged_in'] = True

    return redirect('home')


@app.route('/home')
@is_logged_in
def home():
    user = User.query.filter_by(name=session['name']).first()

    payment_url = f"{os.environ['PAYMENT_URL']}/pay?user={user.name}&callback={os.environ['CALLBACK_URL']}&nonce={user.nonce + 1}"

    return render_template('home.html', user=user, flag=url_for('flag'), payment=payment_url)

@app.route('/flag')
@is_logged_in
def flag():
    user = User.query.filter_by(name=session['name']).first()

    if user and user.balance >= 1337:
        with open('flag.txt', 'r') as f:
            return f.read()

    return "Insufficient balance", 400

@app.route('/callback')
@is_logged_in
def callback():
    message, signature = b"", b""

    for param in request.args:
        if param == "sig":
            signature = request.args[param].encode()
            continue

        for value in request.args.getlist(param):
            message += param.encode()
            message += value.encode()

    try:
        verify_key.verify(signature, message, encoding='hex')

        user = User.query.filter_by(name=session['name']).first()
        nonce = int(request.args['nonce'])

        if nonce <= user.nonce:
            raise Exception

        user.nonce = nonce
        user.balance += int(request.args.get('amount', 0))
        db.session.commit()
    except:
        traceback.print_exc()
        return "Something went wrong", 400

    return redirect('home')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
