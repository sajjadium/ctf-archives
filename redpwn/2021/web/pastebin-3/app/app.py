import os
import secrets
import sqlite3
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session
)

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_KEY')


def execute(query, params=()):
    con = sqlite3.connect('../db/db.sqlite3')
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    return cur.fetchall()


def check_login(username, password):
    (result,), = execute(
        '''
        SELECT EXISTS(
            SELECT * FROM users WHERE
                username = ? AND
                password = ?
        );
        ''',
        params=(username, password)
    )
    return result


def create_account(username, password):
    if len(username) < 4:
        return (False, 'Username too short.')

    (exists,), = execute(
        '''
        SELECT EXISTS(
            SELECT * FROM users WHERE username = ?
        );
        ''',
        params=(username,)
    )

    if exists:
        return (False, 'Username taken.')

    execute(
        'INSERT INTO users (username, password) VALUES (?, ?);',
        params=(username, password)
    )

    return (True, '')


def create_paste(paste, username):
    paste_id = secrets.token_hex(32)
    execute(
        'INSERT INTO pastes (id, paste, username) VALUES (?, ?, ?);',
        params=(paste_id, paste, username)
    )
    return paste_id


def get_pastes(username):
    return [paste_id[0] for paste_id in execute(
        'SELECT id FROM pastes WHERE username = ?',
        params=(username,)
    )]


def get_paste(paste_id):
    results = execute(
        'SELECT paste FROM pastes WHERE id = ?',
        params=(paste_id,)
    )
    if len(results) < 1:
        return 'Paste not found!'
    return results[0][0]


@app.route('/')
def index():
    if 'username' in session:
        return redirect('/home')
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    success = check_login(
        request.form['username'],
        request.form['password']
    )
    if success:
        session['username'] = request.form['username']
        flash('Logged in successfully!')
        return redirect('/home')
    flash('Incorrect username or password.')
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/home')
    if request.method == 'POST':
        username = request.form['username']
        success, message = create_account(
            username,
            request.form['password']
        )
        if not success:
            flash(message)
            return redirect('/register')
        session['username'] = username
        flash('Account created successfully.')
        return redirect('/home')
    return render_template('register.html')


@app.route('/home')
def home():
    if 'username' not in session:
        return redirect('/')
    return render_template(
        'home.html',
        pastes=get_pastes(session['username'])
    )


@app.route('/create_paste', methods=['POST'])
def create():
    if 'username' not in session:
        return redirect('/')
    paste_id = create_paste(
        request.form['paste'],
        session['username']
    )
    return redirect(f'/view?id={paste_id}')


@app.route('/view', methods=['GET'])
def view():
    paste_id = request.args.get('id')
    return render_template(
        'view.html',
        paste_id=paste_id,
        sandbox_url=os.getenv('SANDBOX_URL')
    )


@app.route('/search')
def search():
    if 'username' not in session:
        return redirect('/')
    if 'query' not in request.args:
        flash('Please provide a query!')
        return redirect('/home')
    query = str(request.args.get('query'))
    results = (
        paste for paste in get_pastes(session['username'])
        if query in get_paste(paste)
    )
    try:
        flash(f'Result found: {next(results)}.')
    except StopIteration:
        flash('No results found.')
    return redirect('/home')


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return redirect('/')


def init():
    # this is terrible but who cares
    execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        );
    ''')
    execute('DROP TABLE users;')
    execute('''
        CREATE TABLE users (
            username TEXT PRIMARY KEY,
            password TEXT
        );
    ''')

    # we also need a table for pastes
    execute('''
        CREATE TABLE IF NOT EXISTS pastes (
            id TEXT PRIMARY KEY,
            paste TEXT,
            username TEXT
        );
    ''')
    execute('DROP TABLE pastes;')
    execute('''
        CREATE TABLE pastes (
            id TEXT PRIMARY KEY,
            paste TEXT,
            username TEXT
        );
    ''')

    # put admin into db
    admin_password = secrets.token_hex(32)
    execute(
        'INSERT OR IGNORE INTO users (username, password) VALUES (?, ?);',
        params=('admin', admin_password)
    )
    execute(
        'UPDATE users SET password = ? WHERE username = ?;',
        params=(admin_password, 'admin')
    )
    create_paste(os.getenv('FLAG'), 'admin')


init()
