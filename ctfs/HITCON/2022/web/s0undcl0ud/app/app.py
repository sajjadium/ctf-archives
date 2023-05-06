from flask import Flask, request, redirect, send_from_directory, g, session, render_template
import sqlite3
import os
import re
import secrets
from operator import attrgetter
from werkzeug.security import safe_join

import mimetypes
import magic

import pickle
import pickletools
from flask.sessions import SecureCookieSessionInterface

_pickle_loads = pickle.loads


def loads_with_validate(data, *args, **kwargs):
    opcodes = pickletools.genops(data)

    allowed_args = ['user_id', 'musics', None]
    if not all(op[1] in allowed_args or
               type(op[1]) == int or
               type(op[1]) == str and re.match(r"^musics/[^/]+/[^/]+$", op[1])
               for op in opcodes):
        return {}

    allowed_ops = ['PROTO', 'FRAME', 'MEMOIZE', 'MARK', 'STOP',
                   'EMPTY_DICT', 'EMPTY_LIST', 'SHORT_BINUNICODE', 'BININT1',
                   'APPEND', 'APPENDS', 'SETITEM', 'SETITEMS']
    if not all(op[0].name in allowed_ops for op in opcodes):
        return {}

    return _pickle_loads(data, *args, **kwargs)


pickle.loads = loads_with_validate


class SessionInterface(SecureCookieSessionInterface):
    serializer = pickle


app = Flask(__name__)
app.secret_key = '___SECRET_KEY___'
app.session_interface = SessionInterface()

mimetypes.init()
AUDIO_MIMETYPES = set(filter(lambda mime: mime.startswith('audio/'),
                             mimetypes.types_map.values()))

#### Database #####


def db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('/tmp/db.sqlite3')
        db.row_factory = sqlite3.Row
    return db


@app.before_first_request
def server_start():
    cursor = db().cursor()
    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS "users" (
        "id"        INTEGER PRIMARY KEY AUTOINCREMENT,
        "username"  TEXT,
        "password"  TEXT
    );
    ''')
    db().commit()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


##### Web App #####

@app.get("/")
def home():
    if 'user_id' not in session:
        return redirect("/login")

    return render_template('index.html', musics=session.get('musics'))


@app.get("/login")
def login():
    return render_template('login.html')


@app.post("/login")
def do_login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if not re.match(r"\w{4,15}", username) or not re.match(r"\w{4,15}", password):
        return "Username or password doesn't match \w{4,15}"

    cursor = db().cursor()
    query = "SELECT id, username, password FROM users WHERE username=?"
    res = cursor.execute(query, (username,)).fetchone()
    if res == None:
        # register
        query = "INSERT INTO users (username, password) VALUES (?, ?)"
        user_id = cursor.execute(query, (username, password,)).lastrowid
        db().commit()
        os.mkdir(safe_join("musics", username))
        session["user_id"] = user_id
        session["musics"] = []
        return redirect("/")
    elif res['password'] == password:
        # login
        musics = list(map(attrgetter('path'),
                          os.scandir(safe_join("musics", username))))
        session["user_id"] = res['id']
        session["musics"] = musics
        return redirect("/")
    else:
        return "Wrong password!"


@app.post("/upload")
def upload():
    if 'user_id' not in session:
        return redirect("/login")

    cursor = db().cursor()
    query = "SELECT username FROM users WHERE id=?"
    user_id = session['user_id']
    username = cursor.execute(query, (user_id,)).fetchone()['username']
    file = request.files.get('file')
    if mimetypes.guess_type(file.filename)[0] in AUDIO_MIMETYPES and \
            magic.from_buffer(file.stream.read(), mime=True) in AUDIO_MIMETYPES:
        file.stream.seek(0)
        filename = safe_join("musics", username, file.filename)
        file.save(filename)
        if filename not in session['musics']:
            session['musics'] = session['musics'] + [filename]
        return redirect("/")

    return "Invalid file type!"


@app.get("/@<username>/<file>")
def music(username, file):
    return send_from_directory(f"musics/{username}", file, mimetype="application/octet-stream")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
