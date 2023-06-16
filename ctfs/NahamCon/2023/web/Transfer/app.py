from flask import Flask, request, render_template, redirect, url_for, flash, g, session, send_file
import io
import base64
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from functools import wraps
import sqlite3
import pickle
import os
import uuid
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
DATABASE = '/tmp/database.db'

login_manager = LoginManager()
login_manager.init_app(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_id' not in session:
            return redirect(url_for('home', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

class User(UserMixin):
    pass

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@login_manager.user_loader
def user_loader(username):
    conn = get_db()
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}'")
    user_data = c.fetchone()
    if user_data is None:
        return
    user = User()
    user.id = user_data[0]
    return user

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        conn = get_db()
        c = conn.cursor()
        c.execute(f"SELECT timestamp FROM activesessions WHERE username='{g.user.id}'")
        timestamp = c.fetchone()[0]
        if datetime.now() - datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f") > timedelta(minutes=5):
            flash('Your session has expired')
            return logout()
        else:
            c.executescript(f"UPDATE activesessions SET timestamp='{datetime.now()}' WHERE username='{g.user.id}'")
            conn.commit()

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/files')
@login_required
def files():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT filename FROM files")
    file_list = c.fetchall()
    return render_template('files.html', files=file_list)

def DBClean(string):
    for bad_char in " '\"":
        string = string.replace(bad_char,"")
    return string.replace("\\", "'")

@app.route('/login', methods=['POST'])
def login_user():
    username = DBClean(request.form['username'])
    password = DBClean(request.form['password'])
    
    conn = get_db()
    c = conn.cursor()
    sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    c.executescript(sql)
    user = c.fetchone()
    if user:
        c.execute(f"SELECT sessionid FROM activesessions WHERE username=?", (username,))
        active_session = c.fetchone()
        if active_session:
            session_id = active_session[0]
        else:
            c.execute(f"SELECT username FROM users WHERE username=?", (username,))
            user_name = c.fetchone()
            if user_name:
                session_id = str(uuid.uuid4())
                c.executescript(f"INSERT INTO activesessions (sessionid, timestamp) VALUES ('{session_id}', '{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}')")
            else:
                flash("A session could be not be created")
                return logout()
        
        session['username'] = username
        session['session_id'] = session_id
        conn.commit()
        return redirect(url_for('files'))
    else:
        flash('Username or password is incorrect')
        return redirect(url_for('home'))

@app.route('/logout', methods=['GET'])
def logout():
    if 'session_id' in session:
        conn = get_db()
        c = conn.cursor()
        c.executescript(f"DELETE FROM activesessions WHERE sessionid=" + session['session_id'])
        conn.commit()
        session.pop('username', None)
        session.pop('session_id', None)
    return redirect(url_for('home'))

@app.route('/download/<filename>/<sessionid>', methods=['GET'])
def download_file(filename, sessionid):
    conn = get_db()
    c = conn.cursor()
    c.execute(f"SELECT * FROM activesessions WHERE sessionid=?", (sessionid,))
    
    active_session = c.fetchone()
    if active_session is None:
        flash('No active session found')
        return redirect(url_for('home'))
    c.execute(f"SELECT data FROM files WHERE filename=?",(filename,))
    
    file_data = c.fetchone()
    if file_data is None:
        flash('File not found')
        return redirect(url_for('files'))

    file_blob = pickle.loads(base64.b64decode(file_data[0]))
    return send_file(io.BytesIO(file_blob), download_name=filename, as_attachment=True)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    flash('Sorry, the administrator has temporarily disabled file upload capability.')
    return redirect(url_for('files'))


def init_db():
    with app.app_context():
        db = get_db()
        c = db.cursor()

        c.execute("CREATE TABLE IF NOT EXISTS users (username text, password text)")
        c.execute("CREATE TABLE IF NOT EXISTS activesessions (sessionid text, username text, timestamp text)")
        c.execute("CREATE TABLE IF NOT EXISTS files (filename text PRIMARY KEY, data blob, sessionid text)")

        c.execute("INSERT OR IGNORE INTO files VALUES ('flag.txt', ?, NULL)",
                  (base64.b64encode(pickle.dumps(b'lol just kidding this isnt really where the flag is')).decode('utf-8'),))
        c.execute("INSERT OR IGNORE INTO files VALUES ('NahamCon-2024-Speakers.xlsx', ?, NULL)",
                  (base64.b64encode(pickle.dumps(b'lol gottem')).decode('utf-8'),))
        db.commit()


if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=False, host="0.0.0.0")
