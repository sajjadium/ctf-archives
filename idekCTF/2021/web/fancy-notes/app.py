from flask import Flask, redirect, request, session, send_from_directory, render_template
import os
import sqlite3
import subprocess

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET', 'secret')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'password')
flag = open('flag.txt', 'r').read()


def init_db():
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)')
    cur.execute('INSERT INTO USERS (username, password) VALUES ("admin", ?)', [ADMIN_PASS])
    cur.execute('CREATE TABLE IF NOT EXISTS notes (title TEXT NOT NULL, content TEXT NOT NULL, owner TEXT NOT NULL)')
    cur.execute('INSERT INTO notes (title, content, owner) VALUES ("flag", ?, 1)', [flag])
    con.commit()
    con.close()


def try_login(username, password):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', [username, password])
    row = cur.fetchone()
    if row:
        return {'id': row[0], 'username': row[1]}


def try_register(username, password):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    try:
        cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', [username, password])
    except sqlite3.IntegrityError:
        return None
    con.commit()
    con.close()
    return True


def find_note(query, user):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT title, content FROM notes WHERE owner = ? AND (INSTR(content, ?) OR INSTR(title,?))', [user, query, query])
    rows = cur.fetchone()
    return rows


def get_notes(user):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT title, content FROM notes WHERE owner = ?', [user])
    rows = cur.fetchall()
    return rows


def create_note(title, content, user):
    con = sqlite3.connect('/tmp/database.db')
    cur = con.cursor()
    cur.execute('SELECT title FROM notes where title=? AND owner=?', [title, user])
    row = cur.fetchone()
    if row:
        return False
    cur.execute('INSERT INTO notes (title, content, owner) VALUES (?, ?, ?)', [title, content, user])
    con.commit()
    con.close()
    return True


@app.before_first_request
def setup():
    try:
        os.remove('/tmp/database.db')
    except:
        pass
    init_db()


@app.after_request
def add_headers(response):
    response.headers['Cache-Control'] = 'no-store'
    return response


@app.route('/')
def index():
    if not session:
        return redirect('/login')
    notes = get_notes(session['id'])
    return render_template('index.html', notes=notes, message='select a note to fancify!')


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
            return redirect('/')
        else:
            return render_template('login.html', message='login failed!')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if try_register(username, password):
            return redirect('/login')
        return render_template('register.html', message='registration failed!')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if not session:
        return redirect('/login')
    if session['username'] == 'admin':
        return 'nah'
    if request.method == 'GET':
        return render_template('create.html')
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if len(title) >= 36 or len(content) >= 256:
            return 'pls no'
        if create_note(title, content, session['id']):
            return render_template('create.html', message='note successfully uploaded!')
        return render_template('create.html', message='you already have a note with that title!')


@app.route('/fancy')
def fancify():
    if not session:
        return redirect('/login')
    if 'q' in request.args:
        def filter(obj):
            return any([len(v) > 1 and k != 'q' for k, v in request.args.items()])
        if not filter(request.args):
            results = find_note(request.args['q'], session['id'])
            if results:
                message = 'here is your 𝒻𝒶𝓃𝒸𝓎 note!'
            else:
                message = 'no notes found!'
            return render_template('fancy.html', note=results, message=message)
        return render_template('fancy.html', message='bad format! Your style params should not be so long!')
    return render_template('fancy.html')


@app.route('/report', methods=['GET', 'POST'])
def report():
    if not session:
        return redirect('/')
    if request.method == 'GET':
        return render_template('report.html')
    url = request.form['url']
    subprocess.Popen(['node', 'bot.js', url], shell=False)
    return render_template('report.html', message='admin visited your url!')
    


app.run('0.0.0.0', 1337)
