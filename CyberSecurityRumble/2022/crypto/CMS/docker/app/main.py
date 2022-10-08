from flask import Flask, request, render_template, redirect, abort, url_for, send_from_directory, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.wrappers import Request
from functools import wraps

import re
import os
import time
import traceback
import threading
import pickle
import random

from secret import key_e, key_d, key_n, flag

admin_name = 'willi_pyjCsgC'

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_URI']
app.config['SQLALCHEMY_POOL_RECYCLE'] = 500
db = SQLAlchemy(app)

### Models ###

class User(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    entries = db.relationship("Entry", back_populates="user")

    def __init__(self, name, password):
        self.name = name
        self.password = password

class Entry(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    hidden = db.Column(db.Boolean, nullable=False)
    user_name = db.Column(db.String(100), db.ForeignKey('user.name'),
        nullable=False)
    user = db.relationship("User", back_populates="entries")

    def __init__(self, content, hidden, user_name):
        self.content = content
        self.hidden = hidden
        self.user_name = user_name

### Setup Database ###

db.create_all()

if not User.query.filter_by(name=admin_name).first():
    willi = User(admin_name, 'notavalidpasswordhash')
    db.session.add(willi)
    db.session.commit()

e = Entry(flag, True, admin_name)
if not Entry.query.filter_by(content=e.content).first():
    db.session.add(e)
    db.session.commit()

e = Entry("""
Hello,

today i want to tell you something about crypto. It's really simple. Especially RSA.

The key consists of 2 public (e, n) and 1 private component (d).

To sign a message you just have to calculate s = m^d mod n. To verify it you have to check that m == s^e mod n.
Thats all. Really simple, right?
I even build my own RSA library which is used in this CMS app.

I use RSA signatures for my session cookies. Go ahead and try to verify your session cookie.
My public parameters are:

n = {}
e = {}
    """.format(key_n, key_e)
    , False, admin_name)
if not Entry.query.filter_by(content=e.content).first():
    db.session.add(e)
    db.session.commit()

### Helper functions ###

def get_username():
    assert len(request.cookies['username'].split('||')) == 2
    return request.cookies['username'].split('||')[0]

def rsa_sign(m, n, d):
    return pow(int.from_bytes(bytearray(m, 'utf-8'), byteorder='big'), d, n)

def rsa_verify(m, s, n, e):
    return int.from_bytes(bytearray(m, 'utf-8'), byteorder='big') == pow(int(s), e, n)

def invalidate_cookie():
    resp = make_response(render_template('cookie.html'), 403)
    resp.set_cookie('username', '', expires=0)
    return resp

### Endpoints ###

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'username' in request.cookies:
            return f(*args, **kwargs)
        else:
            return redirect('/login'), 403
    return wrap

@app.before_request
def security():
    if 'curl' in request.headers['User-Agent']:
        return render_template('curl.html'), 403

@app.before_request
def check_cookie():
    try:
        if request.endpoint == 'images':
            return
        if 'username' in request.cookies:
            m, s = request.cookies['username'].split('||')
            if rsa_verify(m, s, key_n, key_e):
                return
        else:
            return
    except:
        traceback.print_exc()
    
    # Failsafe defaults
    return invalidate_cookie()

@app.route('/')
def index():
    entries = Entry.query.filter_by(user_name=admin_name).filter(Entry.hidden == False).all()
    entries.extend(Entry.query.filter(Entry.user_name != admin_name).filter(Entry.hidden == False).order_by(Entry.id.desc()).limit(20))
    return render_template('index.html', login=url_for('login'), register=url_for('register'), home=url_for('home'), entries=entries)

@app.route('/images/<string:name>')
def images(name):
    return send_from_directory('images', name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
  
    name = request.form.get('name', '')

    if not re.match("^[a-zA-Z0-9_]{1,200}$", name):
        return "The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'", 500

    user = User.query.filter_by(name=name).first()

    if not user:
        return "Invalid username", 404

    if not check_password_hash(user.password, request.form.get('passwd', '')):
        return "Invalid password", 403

    resp = make_response(redirect('home'))
    resp.set_cookie('username', f'{user.name}||{rsa_sign(user.name, key_n, key_d)}', httponly=True, samesite='Strict')
    return resp


@app.route('/logout')
@is_logged_in
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('username', '', expires=0)
    return resp


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    name = request.form.get('name', '')
    passwd = request.form.get('passwd', '')

    if not (name and passwd):
        return "You have to specify username *and* password"

    if not re.match("^[a-zA-Z0-9_]{1,200}$", name):
        return "The username should match this regular expression '^[a-zA-Z0-9_]{1,200}$'"

    user = User.query.filter_by(name=name).first()

    try:
        if user:
            raise Exception
        else:
            user = User(name, generate_password_hash(passwd))
            db.session.add(user)
        db.session.commit()
    except:
        return "Username already taken"

    return redirect('login')

@app.route('/home')
@is_logged_in
def home():
    return render_template('home.html', entries=Entry.query.filter_by(user_name=get_username()).all())

@app.route('/add', methods=['GET', 'POST'])
@is_logged_in
def add_entry():
    if request.method == 'GET':
        return render_template('add.html')
    
    username = get_username()
    content = request.form['content']
    hidden = 'hidden' in request.form

    if not User.query.filter_by(name=username).first():
        return "you are not registered"

    try:
        entry = Entry(content, hidden, username)
        db.session.add(entry)
        db.session.commit()
    except:
        traceback.print_exc()
        return "something went wrong"

    return redirect('/home')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=6000, threaded=True)
