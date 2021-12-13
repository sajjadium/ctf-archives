from flask import Flask, redirect, request, session, send_from_directory, render_template, render_template_string, g, make_response, flash
import os
import sqlite3
import random
import string
import re
import socket
import subprocess


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 's3cr3t_k3y')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'adm1n_pa55w0rd')
FLAG = os.getenv('FLAG', 'idek{test_flag}')


def init_db():
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, is_admin INTEGER)')
    cur.execute('INSERT INTO USERS (username, password, is_admin) VALUES ("admin", ?, 1)', [ADMIN_PASS])
    cur.execute('CREATE TABLE IF NOT EXISTS pastes (id TEXT NOT NULL UNIQUE, title TEXT NOT NULL, content TEXT NOT NULL, owner)')
    cur.execute('INSERT INTO pastes (id, title, content, owner) VALUES ("flag", "flag", ?, "admin")', [FLAG])
    con.commit()
    con.close()


def try_login(username, password):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', [username, password])
    row = cur.fetchone()
    if row:
        return {'id': row[0], 'username': row[1], 'is_admin': row[3]}


def try_register(username, password):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)', [username, password])
    except sqlite3.IntegrityError:
        return None
    con.commit()
    con.close()
    return True


def get_all_pastes(username, is_admin=False):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT id, title FROM pastes WHERE owner = ?', [username])
    rows = cur.fetchall()
    if is_admin and username != 'admin':
        cur.execute('SELECT id, title FROM pastes WHERE owner = "admin"')
        admin_rows = cur.fetchall()
        rows += admin_rows
    return rows

def get_paste(username, paste_id, is_admin=False):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    if is_admin:
        cur.execute('SELECT title, content FROM pastes WHERE id = ?', [paste_id])
    else:
        cur.execute('SELECT title, content FROM pastes WHERE id = ? AND owner = ?', [paste_id, username])
    row = cur.fetchone()
    if row:
        return {'title': row[0], 'content': row[1]}

    
def create_paste(username, title, content):
    paste_id = gen_token()
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('INSERT INTO pastes (id, title, content, owner) VALUES (?, ?, ?, ?)', [paste_id, title, content, username])
    con.commit()
    con.close()
    return paste_id


def gen_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(32))


@app.before_first_request
def setup():
    try:
        os.remove('/tmp/database.db')
    except:
        pass
    init_db()


@app.before_request
def add_flashes():
    if 'error' in request.args.keys():
        msg = request.args['error'].lower()

        # no event handlers
        if all(bad_string in msg for bad_string in ['on', '=']):
            return
        # none of this shit
        if any(bad_string in msg for bad_string in ['script', 'svg', 'object', 'img', '/', ':', '>']):
            return

        flash(msg)


@app.route('/')
def index():
    if not session:
        return redirect('/login')
    pastes = get_all_pastes(session['username'])
    return render_template('index.html', pastes=pastes)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        password = request.form['password']
        username = request.form['username']
        user = try_login(username, password)
        if user:
            session['id'] = user['id']
            session['username'] = user['username']
            session['is_admin'] = user['is_admin']
            return redirect('/')
        return redirect('/login?error=login failed')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if try_register(username, password):
            return redirect('/login')
        return redirect('/register?error=registration failed')


@app.route('/pastes/<paste_id>')
def show_paste(paste_id):
    if not session:
        return redirect('/login?error=Please log in')
    paste = get_paste(session['username'], paste_id, is_admin=session['is_admin'])
    return render_template('view_paste.html', paste=paste)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session:
        return redirect('/login?error=Please log in')
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        if session['username'] == 'admin':
            return 'Admin may not create new pastes'
        if not all([field in request.form for field in ['title', 'content']]):
            return 'Missing fields!'
        title = request.form['title']
        content = request.form['content']
        if len(title) > 12:
            flash('Title must not be longer than 12 characters!')
            return redirect('/create')
        if len(content) > 256:
            flash('Content must not be longer than 256 characters!')
            return redirect('/create')
        paste_id = create_paste(session['username'], title, content)
        return redirect(f'/pastes/{paste_id}')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if not session:
        return redirect('/login?error=Please log in')
    if request.method == 'GET':
        return render_template('report.html')

    url = request.form.get('url')
    if not url:
        flash('url is required')
        return render_template('report.html')
    if not url.startswith('http://'):
        flash('invalid url')
        return render_template('report.html')
    subprocess.Popen(['node', 'bot.js', url], shell=False)
    flash('Admin is visiting your link!')
    return render_template('report.html')


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1337, threaded=True)
