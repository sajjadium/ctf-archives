import logging
import os
import re
import sqlite3
import subprocess
import uuid
import zipfile

from flask import (Flask, flash, redirect, render_template, request, abort,
                   send_from_directory, session)
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
DATA_DIR = "/tmp/"

# Uploads can only be 2MB in size
app.config['MAX_CONTENT_LENGTH'] = 2 * 1000 * 1000

# Configure logging
LOG_HANDLER = logging.FileHandler(DATA_DIR + 'server.log')
LOG_HANDLER.setFormatter(logging.Formatter(fmt="[{levelname}] [{asctime}] {message}", style='{'))
logger = logging.getLogger("application")
logger.addHandler(LOG_HANDLER)
logger.propagate = False
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(level=logging.WARNING, format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger().addHandler(logging.StreamHandler())

# Set secret key
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    with sqlite3.connect(DATA_DIR + "database.db") as db:
        res = db.cursor().execute("SELECT password, admin FROM users WHERE username=?", (username,))
        user = res.fetchone()
        if not user or not check_password_hash(user[0], password):
            flash("Incorrect username/password", "danger")
            return render_template("login.html")
    
    session["uid"] = username
    session["admin"] = user[1]
    return redirect("/upload")


@app.route("/register", methods=["GET", "POST"])
def register():
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not username or not password or not re.fullmatch("[a-zA-Z0-9_]{1,24}", username):
        flash("Invalid username/password", "danger")
        return render_template("register.html")
    
    with sqlite3.connect(DATA_DIR + "database.db") as db:
        res = db.cursor().execute("SELECT username FROM users WHERE username=?", (username,))
        if res.fetchone():
            flash("That username is already registered", "danger")
            return render_template("register.html")
        
        db.cursor().execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, generate_password_hash(password)))
        db.commit()
    
    session["uid"] = username
    session["admin"] = False
    return redirect("/upload")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if not session.get("uid"):
        return redirect("/login")
    if request.method == "GET":
        return render_template("upload.html")

    if "file" not in request.files:
        flash("You didn't upload a file!", "danger")
        return render_template("upload.html")
    
    file = request.files["file"]
    uuidpath = str(uuid.uuid4())
    filename = f"{DATA_DIR}uploadraw/{uuidpath}.zip"
    file.save(filename)
    subprocess.call(["unzip", filename, "-d", f"{DATA_DIR}uploads/{uuidpath}"])    
    flash(f'Your unique ID is <a href="/uploads/{uuidpath}">{uuidpath}</a>!', "success")
    logger.info(f"User {session.get('uid')} uploaded file {uuidpath}")
    return redirect("/upload")


@app.route("/uploads/<path:path>")
def uploads(path):
    try:
        return send_from_directory(DATA_DIR + "uploads", path)
    except PermissionError:
        abort(404)


@app.route("/flag")
def flag():
    if not session.get("admin"):
        return "Unauthorized!"
    return subprocess.run("./flag", shell=True, stdout=subprocess.PIPE).stdout.decode("utf-8")
