import asyncio
import hashlib
import hmac
import time
import uuid
import base64
import socket
from datetime import datetime
from logzero import logger
from functools import wraps
import sqlite3
from threading import Thread
from flask import Flask, render_template, g, url_for, request, Response

# run the server: python -m flask run --host=0.0.0.0 --port=5000

SECRET = open('/tmp/secret', 'rb').read()

DATABASE = 'sqlite.db'
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def redirect(location):
    "drop-in replacement for flask's redirect that doesn't sanitize the redirect target URL"
    response = Response(f'Redirecting... to {location}', 302, mimetype="text/html")
    response.headers["Location"] = location
    response.headers["Content-Type"] = 'text/plain'
    response.autocorrect_location_header = False
    return response


def signature(s):
    '''
    generate a hmac signature for a given string
    '''
   
    m = hmac.new(SECRET, digestmod=hashlib.sha256)
    m.update(s.encode('ascii'))
    return m.hexdigest()

def get_db():
    '''
    helper function to get a sqlite database connection
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    '''
    helper function to close the database connection
    '''
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    '''
    helper function to do a SQL query like select
    '''
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def commit_db(query, args=()):
    '''
    helper function to do SQl queries like insert into
    '''
    get_db().cursor().execute(query, args)
    get_db().commit()

def login_required(f):
    '''
    login required decorator to ensure g.user exists
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in g or g.user == None:
            return redirect('/logout')
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def before_request():
    '''
    session middleware. checks if we have a valid session and sets g.user
    '''
    # request - flask.request
    if 'session' not in request.cookies:
        return None
    session = request.cookies['session'].split('.')
    if not len(session) == 2:
        return None
    
    key, sig = session
    if not hmac.compare_digest(sig, signature(key)):
        return None
    g.user= query_db('select * from users where uuid = ?', 
                    [key], one=True)
    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    response = redirect("/")
    response.set_cookie('session', '', expires=0)
    return response

@app.route('/notes')
@login_required
def notes():
    order = request.args.get('order', 'desc')
    notes = query_db(f'select * from notes where user = ? order by timestamp {order}', [g.user['uuid']])
    return render_template('notes.html', user=g.user, notes=notes)


@app.route('/delete_note', methods=['POST'])
@login_required
def delete_note():
    user = g.user['uuid']
    note_uuid = request.form['uuid']
    commit_db('delete from notes where uuid = ? and user = ?', [note_uuid, user])
    return redirect(f'/notes?deleted={note_uuid}')

@app.route('/add_note', methods=['POST'])
@login_required
def add_note():
    new_note_uuid = uuid.uuid4().hex
    user = g.user['uuid']
    title = request.form['title']
    body = request.form['body']

    commit_db('insert into notes (uuid, user, title, body) values (?, ?, ?, ?)', 
        [new_note_uuid, user, title, body])
    return redirect('/notes')

@app.route('/registerlogin', methods=['POST'])
def registerlogin():
    username = request.form['username']
    password = request.form['password']
    pwhash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user = query_db('select * from users where username = ? and password = ?', 
                    [username, pwhash], one=True)

    if not user:
        # new user. let's create it in the database
        new_user_uuid = uuid.uuid4().hex
        commit_db('insert into users (uuid, username, password) values (?, ?, ?)', 
                [new_user_uuid, username, pwhash])
        user= query_db('select * from users where uuid = ?', [new_user_uuid], one=True)
    
    # calculate signature for cookie
    key = user['uuid']
    sig = signature(user['uuid'])
    response = redirect('/notes')
    response.set_cookie('session', f'{key}.{sig}')
    return response

