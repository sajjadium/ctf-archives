import os
import secrets
import sqlite3
import time
from functools import wraps

import bcrypt
import jwt
from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
)

app = Flask(__name__)
app.static_folder = "static"
load_dotenv()
app.config["SECRET_KEY"] = "".join(
    [secrets.choice("abcdef0123456789") for _ in range(32)]
)
FLAG = os.getenv("FLAG")


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE IF EXISTS employees;""")
    cursor.execute("""DROP TABLE IF EXISTS revoked_tokens;""")
    cursor.execute("""DROP TABLE IF EXISTS users;""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        is_admin BOOL NOT NULL,
                        password_hash TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS revoked_tokens (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        token TEXT NOT NULL)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        position TEXT NOT NULL,
                        phone TEXT NOT NULL,
                        location TEXT NOT NULL)""")
    conn.commit()
    conn.close()


def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get("JWT")
        if not token:
            flash("Token is missing!", "error")
            return redirect("/login")

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            username = data["username"]

            conn = get_db_connection()
            user = conn.execute(
                "SELECT id,is_admin FROM users WHERE username = ?", (username,)
            ).fetchone()
            revoked = conn.execute(
                "SELECT id FROM revoked_tokens WHERE token = ?", (token,)
            ).fetchone()
            conn.close()

            if not user or revoked:
                flash("Invalid or revoked token!", "error")
                return redirect("/login")

            request.is_admin = user["is_admin"]
            request.username = username

        except jwt.InvalidTokenError:
            flash("Invalid token!", "error")
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated


@app.route("/", methods=["GET"])
def index():
    token = request.cookies.get("JWT", None)
    if token is None:
        return redirect("/login")
    else:
        return redirect("/employees")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Username and password required!"}), 400

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO users (username, is_admin, password_hash) VALUES (?, ?, ?)",
                (username, False, password_hash),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("User already exists.", "error")
            return redirect("/register")
        finally:
            conn.close()

        flash("User created successfully.", "success")
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()

        if user and bcrypt.checkpw(
            password.encode("utf-8"), user["password_hash"].encode("utf-8")
        ):
            token = jwt.encode(
                {
                    "username": username,
                    "is_admin": user["is_admin"],
                    "issued": time.time(),
                },
                app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            resp = make_response(redirect("/employees"))
            resp.set_cookie("JWT", token)
            return resp

        flash("Invalid credentials.", "error")
        return redirect("/login")


@app.route("/logout", methods=["GET"])
def logout():
    token = request.cookies.get("JWT")
    if token:
        conn = get_db_connection()
        conn.execute("INSERT INTO revoked_tokens (token) VALUES (?)", (token,))
        conn.commit()
        conn.close()
    resp = make_response(redirect("/login"))
    resp.delete_cookie("JWT")
    return resp


@app.route("/employees", methods=["GET"])
@token_required
def employees():
    query = request.args.get("query", "")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT id, name, email, position FROM employees WHERE name LIKE '%{query}%'"
    )
    results = cursor.fetchall()
    conn.close()
    print(request.username)
    return render_template("employees.html", username=request.username, employees=results, query=query)


@app.route("/employee/<int:employee_id>", methods=["GET"])
@token_required
def employee_details(employee_id):
    conn = get_db_connection()
    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?", (employee_id,)
    ).fetchone()
    conn.close()
    print(employee)
    if not employee:
        flash("Employee not found", "error")
        return redirect("/employees")
    return render_template("employee_details.html", username=request.username, employee=employee)


@app.route("/admin", methods=["GET"])
@token_required
def admin():
    is_admin = getattr(request, "is_admin", None)
    if is_admin:
        return render_template("admin.html", username=request.username, flag=FLAG)

    flash("You don't have the permission to access this area", "error")
    return redirect("/employees")


if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5000)
