from flask import Flask, render_template, url_for, request, redirect, session
from flask_session import Session
import os
import sqlite3
import subprocess

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    cur = get_db_connection().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def verifyUser(admin=False):
    username = session.get("username")
    if not username:
        return False
    conn = get_db_connection()
    user = query_db("SELECT * FROM users WHERE username = ?",
            [username],
            one=True)
    conn.close()
    if user is None:
        return False
    
    return not admin or user['admin'] == True

@app.route('/admin')
def admin():
    if not verifyUser(admin=True):
        return render_template("403.html"), 403
    
    comments = query_db("SELECT * FROM comments")
    return render_template("admin.html", comments=comments)

@app.route('/updatePassword', methods=['POST'])
def updatePassword():
    if not verifyUser(admin=True):
        return render_template("403.html"), 403
    
    newPassword = request.form['newPassword']

    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute(f"UPDATE users SET password = '{newPassword}' WHERE username = '{session.get('username')}'")
    connection.commit()
    connection.close()
    return "Success<br>Your password has been changed<br><a href='/admin'>Back</a>" 


@app.route('/resetDB', methods=['POST'])
def resetDB():
    if not verifyUser(admin=True):
        return render_template("403.html"), 403
    
    result = subprocess.run(f"python init_db.py {session.get('username')}", shell=True)
    if result.returncode != 0:
        return "DB RESET FAILED<br>Note: your password has changed<br><a href='/admin'>Back</a>"
    else:
        return "Success<br>Note: your password has changed<br><a href='/admin'>Back</a>"





@app.route('/')
def index():
    if not verifyUser():
        return redirect(url_for("login"))

    comments = query_db("SELECT * FROM comments WHERE username = ?",
            [session.get("username")])
    return render_template("index.html", comments=comments)

@app.route('/contact', methods=['POST'])
def contact():
    if not verifyUser():
        return redirect(url_for("login"))
    
    comment = request.form['comment']
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO comments (username, content) VALUES (?, ?)",
        (session.get("username"), comment)
        )
    conn.commit()
    conn.close()

    return render_template("submitted.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['name']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return render_template('signup.html', message="Error: passwords do not match!")
        
        user = query_db("SELECT * FROM users WHERE username = ?",
            [username],
            one=True)

        if user is not None:
            return render_template('signup.html', message="Error: user already exists.")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
            (email, username, password)
            )
        conn.commit()
        conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('signup.html', message="")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']
        
        user = query_db("SELECT * FROM users WHERE username = ? AND password = ?",
            [username, password],
            one=True)

        if user is None:
            return render_template('login.html', message="Error: invalid username or password.")

        session["username"] = username
        return redirect(url_for('index'))
    
    return render_template('login.html', message="")

@app.route("/logout")
def logout():
    session["username"] = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
