from flask import (
    Flask,
    request,
    render_template_string,
    session,
    redirect,
    send_file
)
from random import SystemRandom
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_KEY')

rand = SystemRandom()

allowed_characters = set(
    'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
)


def execute(query):
    con = sqlite3.connect('db/db.sqlite3')
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return cur.fetchall()


def generate_token():
    return ''.join(
        rand.choice(list(allowed_characters)) for _ in range(32)
    )


def create_user(username, password):
    if any(c not in allowed_characters for c in username):
        return (False, 'Alphanumeric usernames only, please.')
    if len(username) < 1:
        return (False, 'Username is too short.')
    if len(password) > 50:
        return (False, 'Password is too long.')
    other_users = execute(
        f'SELECT * FROM users WHERE username=\'{username}\';'
    )
    if len(other_users) > 0:
        return (False, 'Username taken.')
    execute(
        'INSERT INTO users (username, password)'
        f'VALUES (\'{username}\', \'{password}\');'
    )
    return (True, '')


def check_login(username, password):
    if any(c not in allowed_characters for c in username):
        return False
    correct_password = execute(
        f'SELECT password FROM users WHERE username=\'{username}\';'
    )
    if len(correct_password) < 1:
        return False
    return correct_password[0][0] == password


@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        valid_login = check_login(
            request.form['username'],
            request.form['password']
        )
        if valid_login:
            session['username'] = request.form['username']
            return redirect('/message')
        error = 'Incorrect username or password.'
    if 'username' in session:
        return redirect('/message')
    return render_template_string('''
        <link rel="stylesheet" href="/static/style.css" />
        <div class="container">
            <p>Log in to see Aaron's message!</p>
            <form method="POST">
                <label for="username">Username</label>
                <input type="text" name="username" />
                <label for="password">Password</label>
                <input type="password" name="password" />
                <input type="submit" value="Log In" />
            </form>
            <p>{{ error }}</p>
            <a href="/register">Register</a>
        <div class="container">
    ''', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        success, message = create_user(
            request.form['username'],
            request.form['password']
        )
        if success:
            session['username'] = request.form['username']
            return redirect('/message')
    return render_template_string('''
        <link rel="stylesheet" href="/static/style.css" />
        <div class="container">
            <p>Register!</p>
            <form method="POST">
                <label for="username">Username</label>
                <input type="text" name="username" />
                <label for="password">Password</label>
                <input type="password" name="password" />
                <input type="submit" value="Register" />
            </form>
            <p>{{ error }}</p>
        </div>
    ''', error=message)


@app.route('/message')
def message():
    if 'username' not in session:
        return redirect('/')
    if session['username'] == 'ginkoid':
        return send_file(
            'flag.mp3',
            attachment_filename='flag-at-end-of-file.mp3'
        )
    return '''
        <link rel="stylesheet" href="/static/style.css" />
            <div class="container">
            <p>You are logged in!</p>
            <p>Unfortunately, Aaron's message is for cool people only.</p>
            <p>(like ginkoid)</p>
            <a href="/logout">Log out</a>
        </div>
    '''


@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/')
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

    # put ginkoid into db
    ginkoid_password = generate_token()
    execute(
        'INSERT OR IGNORE INTO users (username, password)'
        f'VALUES (\'ginkoid\', \'{ginkoid_password}\');'
    )
    execute(
        f'UPDATE users SET password=\'{ginkoid_password}\''
        f'WHERE username=\'ginkoid\';'
    )


init()
