from flask import Flask, request, session, redirect, url_for, flash, abort, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from secret import SIG_KEY
from functools import wraps
import traceback
import re
import sys

app = Flask(__name__)

with open('/secret', 'rb') as f:
    app.secret_key = f.read(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb+pymysql://root:cybercyber@payment-database/payment'
app.config['SESSION_COOKIE_NAME'] = 'payment'
db = SQLAlchemy(app)



### Models ###

class User(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    balance = db.Column(db.BigInteger, nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.balance = 0

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

    if 'next' in request.args and request.args['next'] != '':
        return redirect(request.args['next'])

    print('ok', file=sys.stderr, flush=True)

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

    if 'next' in request.args and request.args['next'] != '':
        return redirect(request.args['next'])

    return redirect('home')

@app.route('/home')
@is_logged_in
def home():
    user = User.query.filter_by(name=session['name']).first()

    return render_template('home.html', user=user)

@app.route('/pay', methods=['GET', 'POST'])
def pay():
    if 'logged_in' not in session:
        return redirect(url_for('login', next=request.url))

    if request.method == "GET":
        return render_template('amount.html')

    amount = int(request.form.get('amount', 0))

    user = User.query.filter_by(name=session['name']).first()

    if amount > user.balance:
        return "Insufficient balance", 400

    if amount < 0:
        return "Invalid amount", 400

    cb = request.args['callback']
    u = request.args['user']
    nonce = request.args['nonce']

    m = f"user{u}amount{amount}nonce{nonce}".encode()

    sig = SIG_KEY.sign(m, encoding='hex')

    user.balance -= amount
    db.session.commit()

    return redirect(f"{cb}/callback?user={u}&amount={amount}&nonce={nonce}&sig={sig.decode()}", code=302)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
