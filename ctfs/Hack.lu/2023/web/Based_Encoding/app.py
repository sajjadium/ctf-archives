from flask import Flask, redirect, request, session, render_template, flash
import os
import sqlite3
import secrets
import based91
import time
import re

import subprocess


app = Flask(__name__)

base_url = os.getenv("BASE_URL", "http://localhost:5000")
FLAG = os.getenv("FLAG", "flag{testflag}")

admin_password = secrets.token_urlsafe(32)
app.secret_key = secrets.token_bytes(32)


def get_cursor():
    db = sqlite3.connect("/tmp/app.db")
    return db, db.cursor()


def init_db():
    db, cur = get_cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS accounts (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, admin INTEGER)")
    cur.execute("INSERT INTO accounts (username, password, admin) VALUES ('admin', ?, 1)", [admin_password])
    cur.execute("CREATE TABLE IF NOT EXISTS encodings (id TEXT NOT NULL UNIQUE, text TEXT NOT NULL, creator, expires INTEGER DEFAULT 0)")
    cur.execute("INSERT INTO encodings (id, text, creator, expires) VALUES (?, ?, 'admin', 0)", [secrets.token_hex(20), FLAG])
    db.commit()
    db.close()
if not os.path.isfile("/tmp/app.db"):
    init_db()


def signup_db(username, password):
    db, cursor = get_cursor()
    try:
        cursor.execute("INSERT INTO accounts (username, password, admin) VALUES (?, ?, 0)", [username, password])
    except sqlite3.IntegrityError:
        return False
    db.commit()
    return True

def login_db(username, password):
    db, cursor = get_cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", [username, password])
    result = cursor.fetchone()
    if not result: return None
    return {"id": result[0], "username": result[1], "admin": result[3] == 1}


def get_encodings(username):
    db, cursor = get_cursor()
    cursor.execute("SELECT id, text, expires FROM encodings WHERE creator = ?", [username])
    rows = cursor.fetchall()
    for i, row in enumerate(rows):
        if row[2] > 0 and row[2] < int(time.time()):
            cursor.execute("DELETE FROM encodings WHERE id = ?", [row[0]])
            db.commit()
            rows[i] = None
    return [row for row in rows if row is not None]

def get_encoding(msg_id):
    db, cursor = get_cursor()
    cursor.execute("SELECT text, creator, expires FROM encodings WHERE id = ?", [msg_id])
    row = cursor.fetchone()
    if row is None: return None
    if row[2] > 0 and row[2] < int(time.time()):
        cursor.execute("DELETE FROM encodings WHERE id = ?", [msg_id])
        db.commit()
        return None
    return {"text": row[0], "creator": row[1]}
    
def create_encoding(username, text):
    db, cursor = get_cursor()
    id_val = secrets.token_hex(20)
    expires = int(time.time()) + 60 * 60
    cursor.execute("INSERT INTO encodings (id, text, creator, expires) VALUES (?, ?, ?, ?)", [id_val, text, username, expires])
    db.commit()
    return id_val


@app.after_request
def add_header(response):
    response.headers["Content-Security-Policy"] = "script-src 'unsafe-inline';"
    return response

@app.route("/")
def mainRoute():
    if not session:
        return redirect("/login")
    encodings = get_encodings(session["username"])
    return render_template("index.html", encodings=encodings, logged_out=False)


@app.route("/login", methods = ["GET", "POST"])
def login():
    logged_out = session.get("username", None) is None
    if request.method == "GET":
        return render_template("login.html", logged_out=logged_out)
    elif request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]
        user = login_db(username, password)
        if user:
            session["id"] = user["id"]
            session["username"] = user["username"]
            session["admin"] = user["admin"]
            return redirect("/")
        flash("Invalid username or password")
        return redirect("/login")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    logged_out = session.get("username", None) is None
    if request.method == "GET":
        return render_template("signup.html", logged_out=logged_out)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if signup_db(username, password):
            return redirect("/login")
        flash("Username already taken")
        return redirect("/signup")


@app.route("/e/<encoding_id>")
def getEncoding(encoding_id):
    logged_out = session.get("username", None) is None
    encoding = get_encoding(encoding_id)
    return render_template("view_encoding.html", encoding=encoding, logged_out=logged_out)


@app.route("/create", methods=["GET", "POST"])
def create():
    if not session:
        flash("Please log in")
        return redirect("/login")
    if request.method == "GET":
        return render_template("create.html", logged_out=False)
    elif request.method == "POST":
        if not request.form["text"]:
            return "Missing text"
        text = request.form["text"]
        if len(text) > 1000:
            flash("Too long!")
            return redirect("/create")
        encoded = based91.encode(text.encode() if not (re.match(r"^[a-f0-9]+$", text) and len(text) % 2 == 0) else bytes.fromhex(text))
        encoding_id = create_encoding(session["username"], encoded)
        
        return redirect(f"/e/{encoding_id}")

@app.route("/report", methods=["GET", "POST"])
def report():
    if not session:
        flash("Please log in")
        return redirect("/login")
    if request.method == "GET":
        return render_template("report.html", logged_out=False)

    value = request.form.get("id")

    if not value or not re.match(r"^[a-f0-9]{40}$", value):
        flash("invalid value!")
        return render_template("report.html", logged_out=False)
    subprocess.Popen(["timeout", "-k" "15", "15", "node", "adminbot.js", base_url, admin_password, value], shell=False)
    flash("An admin going there.")
    return render_template("report.html", logged_out=False)


# app.run(host="0.0.0.0", port=5000, threaded=True)
