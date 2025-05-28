import requests
from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    abort,
    url_for,
    make_response,
)
from models import db, Users
from sqlalchemy_utils import database_exists
from sqlalchemy.exc import OperationalError
import socket
import time


app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)

# Connect to sage
sage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sage.setblocking(False)
addr = ("localhost", 5000)
try:
    # Attempt to connect to the server
    sage.connect(addr)
except BlockingIOError:
    # Non-blocking sockets may raise a BlockingIOError if the connection is still in progress
    pass

# You can continue with other tasks or use a loop to check the connection status
connected = False
while not connected:
    try:
        # Attempt to complete the connection
        sage.connect(addr)
        connected = True
    except ConnectionRefusedError:
        print("Connection refused. Server may not be available.")
        break
    except BlockingIOError:
        # Connection is still in progress; you can perform other tasks here
        pass


def recvline(sock, buffer_size=1):
    """
    Receive a line of text from a socket.

    :param sock: The socket to receive data from.
    :param buffer_size: The size of the buffer for receiving data.
    :return: The received line as a string, or None if the connection is closed.
    """
    data = b""  # Initialize an empty bytes string to store received data.
    while True:
        while True:
            try:
                chunk = sock.recv(buffer_size)  # Receive data in chunks.
                break
            except BlockingIOError:
                time.sleep(1)
        if not chunk:
            # If no more data is received, the connection is closed.
            if data:
                return data
            else:
                return None

        data += chunk
        if b"\n" in data:
            return data


time.sleep(3)


def menu_eating():
    for _ in range(6):
        print(recvline(sage), flush=True)


menu_eating()


def secret_encrypt(secret):
    sage.send(b"3\n")
    print(recvline(sage), flush=True)
    sage.send(secret.encode() + b"\n")
    resp = recvline(sage).decode().strip()
    print(resp, flush=True)
    enc_secret = hex(int(resp, 16))
    menu_eating()
    return enc_secret


def authed():
    return bool(session.get("id", False))


with app.app_context():
    if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]) is False:
        try:
            db.create_all()
        except OperationalError:
            pass
        admin = Users.query.filter_by(username="admin").first()
        if admin is None:
            admin = Users("admin", "admin")
            admin.password = "admin"
            db.session.add(admin)
            db.session.commit()


@app.context_processor
def inject_user():
    if session:
        return dict(session)
    return dict()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        errors = []
        user = Users.query.filter_by(username=username).first()
        if user:
            if user.password == password:
                session["id"] = user.id
                session["username"] = user.username
                resp = make_response(redirect("/"))
                if session["username"] != "admin":
                    message = (b"This is not the admin secret!").hex()
                else:
                    message = (app.config.get("FLAG")).hex()
                resp.set_cookie("secret", secret_encrypt(message))
                resp.set_cookie("input", "00")
                return resp
            else:
                errors.append("That password doesn't match what we have")
                return render_template("login.html", errors=errors)
        else:
            errors.append("Couldn't find a user with that username")
            return render_template("login.html", errors=errors)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        confirm = request.form.get("confirm").strip()
        errors = []
        if password != confirm:
            errors.append("Your passwords do not match")
        if len(password) < 5:
            errors.append("Your password must be longer")
        exists = Users.query.filter_by(username=username).first()
        if exists:
            errors.append("That username is taken")
        if errors:
            return render_template("register.html", username=username, errors=errors)
        user = Users(username, password)
        db.session.add(user)
        db.session.commit()
        db.session.flush()
        session["id"] = user.id
        session["username"] = user.username
        db.session.close()
        resp = make_response(redirect("/"))
        message = (b"This is not the admin secret!").hex()
        resp.set_cookie("secret", secret_encrypt(message))
        resp.set_cookie("input", "00")
        return resp


@app.route("/encrypt", methods=["GET"])
def encrypt():
    if not authed():
        return redirect("/login")
    else:
        sage.send(b"1\n")
        print(recvline(sage), flush=True)
        cookie = request.cookies.get("input")
        sage.send((str(cookie) + "\n").encode())
        msg = recvline(sage).decode()
        menu_eating()
        resp = make_response(msg)
        return resp


@app.route("/decrypt", methods=["GET"])
def decrypt():
    if not authed():
        return redirect("/login")
    else:
        sage.send(b"2\n")
        print(recvline(sage), flush=True)
        cookie = request.cookies.get("input")
        sage.send((str(cookie) + "\n").encode())
        msg = recvline(sage).decode()
        menu_eating()
        resp = make_response(msg)
        return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
