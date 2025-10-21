import os
import sqlite3
import secrets
import hashlib
from hashlib import md5
from datetime import datetime, timedelta, timezone

import jwt
from flask import (
    Flask, request, render_template, redirect, session,
    flash, url_for, g, abort, make_response
)

from admin_routes import admin_bp,generate_jwt


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SECRET_DIR = os.path.join(BASE_DIR, 'secret')
FLAG_PATH = os.path.join(SECRET_DIR, 'flag.txt')
FLAG_PREFIX = 'QnQsec'


def ensure_flag():
    os.makedirs(SECRET_DIR, exist_ok=True)
    if not os.path.exists(FLAG_PATH):
        with open(FLAG_PATH, 'w') as f:
            f.write(f"{FLAG_PREFIX}{{{secrets.token_hex(16)}}}")


ensure_flag()


app = Flask(__name__)
base = os.environ.get("Q_SECRET", "qnqsec-default")
app.config['SECRET_KEY'] = hashlib.sha1(("pepper:" + base).encode()).hexdigest()


app.config['JWT_SECRET'] = hashlib.sha256(("jwtpepper:" + base).encode()).hexdigest()
app.config['JWT_EXPIRES_MIN'] = 60


app.register_blueprint(admin_bp)


DB_PATH = os.path.join(BASE_DIR, 'users.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH, timeout=10)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH, timeout=10) as db:
        db.execute('PRAGMA journal_mode=WAL')
        db.execute('drop table if exists users')
        db.execute('create table users(username text primary key, password text not null)')
        
        db.execute('insert into users values("flag", "401b0e20e4ccf7a8df254eac81e269a0")')
        db.commit()


if not os.path.exists(DB_PATH):
    init_db()


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html')

    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''
    if not username or not password:
        flash('Missing username or password', 'error')
        return render_template('sign_up.html')

    try:
        db = get_db()
        db.execute(
            'insert into users values(lower(?), ?)',
            (username, md5(password.encode()).hexdigest())
        )
        db.commit()
        flash(f'User {username} created', 'message')
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
        flash('Username is already registered', 'error')
        return render_template('sign_up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = (request.form.get('username') or '').strip()
    password = request.form.get('password') or ''
    if not username or not password:
        flash('Missing username or password', 'error')
        return render_template('login.html')

    db = get_db()
    row = db.execute(
        'select username, password from users where username = lower(?) and password = ?',
        (username, md5(password.encode()).hexdigest())
    ).fetchone()

    if row:
        session['user'] = username.title()

        
        role = "admin" if username.lower() == "flag" else "user"
        token = generate_jwt(session['user'],role,app.config['JWT_EXPIRES_MIN'],app.config['JWT_SECRET'])

        resp = make_response(redirect(url_for('account')))
        resp.set_cookie("admin_jwt", token, httponly=False, samesite="Lax")
        return resp

    flash('Invalid username or password', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie("admin_jwt")
    return resp


@app.route('/account')
def account():
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))
    if user == 'Flag':
        return render_template('account.html', user=user, is_admin=True)
    return render_template('account.html', user=user, is_admin=False)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
