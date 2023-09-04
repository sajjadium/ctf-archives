from flask import Flask, render_template, request, redirect, url_for, session, g, send_from_directory
import mimetypes
import requests
import imageio
import os
import sqlite3
import hashlib
import re
from shutil import copyfile, rmtree
import numpy as np

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
DATABASE = 'mosaic.db'
UPLOAD_FOLDER = 'uploads'
MOSAIC_FOLDER = 'static/uploads'

if os.path.exists("/flag.png"):
    FLAG = "/flag.png"
else:
    FLAG = "/test-flag.png"

try:
    with open("password.txt", "r") as pw_fp:
        ADMIN_PASSWORD = pw_fp.read()
        pw_fp.close()
except:
    ADMIN_PASSWORD = "admin"

def apply_mosaic(image, output_path, block_size=10):
    height, width, channels = image.shape
    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            block = image[y:y+block_size, x:x+block_size]
            mean_color = np.mean(block, axis=(0, 1))
            image[y:y+block_size, x:x+block_size] = mean_color
    imageio.imsave(output_path, image)

def hash(password):
    return hashlib.md5(password.encode()).hexdigest()

def type_check(guesstype):
    return guesstype in ["image/png", "image/jpeg", "image/tiff", "application/zip"]

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def init_db():
    with app.app_context():
        db = get_db()
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT unique, password TEXT)")
        db.execute(f"INSERT INTO users (username, password) values('admin', '{hash(ADMIN_PASSWORD)}')")
        db.commit()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['GET'])
def index():
    if not session.get('logged_in'):
        return '''<h1>Welcome to my mosiac service!!</h1><br><a href="/login">login</a>&nbsp;&nbsp;<a href="/register">register</a>'''
    else:
        if session.get('username') == "admin" and request.remote_addr == "127.0.0.1":
            copyfile(FLAG, f'{UPLOAD_FOLDER}/{session["username"]}/flag.png')
        return '''<h1>Welcome to my mosiac service!!</h1><br><a href="/upload">upload</a>&nbsp;&nbsp;<a href="/mosaic">mosaic</a>&nbsp;&nbsp;<a href="/logout">logout</a>'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not re.match('^[a-zA-Z0-9]*$', username):
            return "Plz use alphanumeric characters.."
        cur = get_db().cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash(password)))
        get_db().commit()
        os.mkdir(f"{UPLOAD_FOLDER}/{username}")
        os.mkdir(f"{MOSAIC_FOLDER}/{username}")
        return redirect(url_for('login'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not re.match('^[a-zA-Z0-9]*$', username):
            return "Plz use alphanumeric characters.."
        cur = get_db().cursor()
        user = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hash(password))).fetchone()
        if user:
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials. Please try again.'
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/mosaic', methods=['GET', 'POST'])
def mosaic():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        image_url = request.form.get('image_url')
        if image_url and "../" not in image_url and not image_url.startswith("/"):
            guesstype = mimetypes.guess_type(image_url)[0]
            ext = guesstype.split("/")[1]
            mosaic_path = os.path.join(f'{MOSAIC_FOLDER}/{session["username"]}', f'{os.urandom(8).hex()}.{ext}')
            filename = os.path.join(f'{UPLOAD_FOLDER}/{session["username"]}', image_url)
            if os.path.isfile(filename):
                image = imageio.imread(filename)
            elif image_url.startswith("http://") or image_url.startswith("https://"):
                return "Not yet..! sry.."
            else:
                if type_check(guesstype):
                    image_data = requests.get(image_url, headers={"Cookie":request.headers.get("Cookie")}).content
                    image = imageio.imread(image_data)
            
            apply_mosaic(image, mosaic_path)
            return render_template("mosaic.html", mosaic_path = mosaic_path)
        else:
            return "Plz input image_url or Invalid image_url.."
    return render_template("mosaic.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        filename = os.path.basename(file.filename)
        guesstype = mimetypes.guess_type(filename)[0]
        image_path = os.path.join(f'{UPLOAD_FOLDER}/{session["username"]}', filename)
        if type_check(guesstype):
            file.save(image_path)
            return render_template("upload.html", image_path = image_path)
        else:
            return "Allowed file types are png, jpeg, jpg, zip, tiff.."
    return render_template("upload.html")

@app.route('/check_upload/@<username>/<file>')
def check_upload(username, file):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if username == "admin" and session["username"] != "admin":
        return "Access Denied.."
    else:
        return send_from_directory(f'{UPLOAD_FOLDER}/{username}', file)

if __name__ == '__main__':
    init_db()
    app.run(host="0.0.0.0", port="9999")