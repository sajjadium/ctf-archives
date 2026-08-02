from flask import Flask, request, redirect, url_for, render_template_string, session
import sqlite3
import random
import string
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
flag = "LITCTF{[redacted]}"

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    characters = string.ascii_letters + string.digits
    randomstring = 'a' + ''.join(random.choice(characters) for _ in range(100))
    c.execute("CREATE TABLE IF NOT EXISTS " + randomstring + " (flag TEXT)")
    c.execute("INSERT INTO " + randomstring + " (flag) VALUES ('" + flag + "')")
    conn.commit()
    conn.close()

init_db()

login_page = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post">
  Username: <input type="text" name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Login">
</form>
<p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
{% if error %}
<p style="color:red">{{ error }}</p>
{% endif %}
"""

register_page = """
<!doctype html>
<title>Register</title>
<h2>Register</h2>
<form method="post">
  Username: <input type="text" name="username"><br><br>
  Password: <input type="password" name="password"><br><br>
  <input type="submit" value="Register">
</form>
<p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
{% if error %}
<p style="color:red">{{ error }}</p>
{% endif %}
"""

home_page = """
<!doctype html>
<title>Home</title>
<h2>Welcome, {{ user }}!</h2>
<a href="{{ url_for('logout') }}">Logout</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username='" + username + "' AND password='" + password + "'")
        user = c.fetchone()
        conn.close()

        if user:
            session["username"] = user[0]
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
    return render_template_string(login_page, error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if not username or not password:
            error = "Both fields are required"
        else:
            try:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password) VALUES ('" + username + "', '" + password + "')")
                conn.commit()
                conn.close()
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                error = "Username already exists"
    return render_template_string(register_page, error=error)

@app.route("/home")
def home():
    if "username" in session:
        return render_template_string(home_page, user=session["username"])
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)