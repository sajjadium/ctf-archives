from flask import Flask, request, redirect, make_response, send_from_directory
from werkzeug.urls import url_decode, url_encode
from functools import wraps
from collections import defaultdict
import hashlib
import requests
import re
import secrets
import base64

app = Flask(__name__)

FLAGMOKER = "REDACTED"
MOKERS = {"moker1": "dQJOyoO", "moker2": "dQJOyoO", "moker3": "dQJOyoO", "moker4": "dQJOyoO", "moker6": "dQJOyoO", "moker7": "dQJOyoO", "moker8": "dQJOyoO", "flagmoker": FLAGMOKER}
MOKER_PATTERN = re.compile("^[A-Za-z0-9]+$")
MOKEROFTHEDAY = "moker3"
STYLE_PATTERN = re.compile("^[A-Za-z0 -9./]+$")
STYLES = ["moker.css", "plain.css"]

########### HELPERS

def imgur(moker):
    return f"https://i.imgur.com/{moker}.png"

ADMIN_PASS = "REDACTED"
users = {"@admin": {"password": ADMIN_PASS, "mokers": []}}
sessions = defaultdict(dict)

@app.after_request
def csp(r):
    # Moker does not like "Java Script"
    r.headers["Content-Security-Policy"] = "script-src 'none'; img-src https://i.imgur.com/"
    return r

def session(f):
    @wraps(f)
    def dec(*a, **k):
        session = request.cookies.get("session", None)
        if session is None or session not in sessions:
            return redirect("/")

        session_obj = sessions[session]
        return f(session_obj, *a, **k)
    return dec

def csrf(f):
    @wraps(f)
    def dec(*a, **k):
        session = request.cookies.get("session", None)
        if session is None or session not in sessions:
            return redirect("/")
        session = sessions[session]

        token = request.args.get("token", None)
        args = base64.urlsafe_b64decode(request.args.get("args", ""))
        if args != b"":
            query = request.path.encode() + b"?" + args
        else:
            query = request.path.encode()

        if token is None:
            return "CSRF token missing"
        if hashlib.sha256(session["key"] + query).digest().hex() != token:
            return "Invalid CSRF token"

        request.args = url_decode(args)
        return f(*a, **k)
    return dec

def signer(session):
    def sign(url):
        raw_url = url.encode()
        token = hashlib.sha256(session["key"] + raw_url).digest().hex()
        if url.find("?") != -1:
            idx = url.index("?")
            base = url[:idx]
            args = url[idx+1:]
            return base + "?" + url_encode({"args": base64.urlsafe_b64encode(args.encode()), "token": token})
        else:
            return url + "?" + url_encode({"args": '', "token": token})
    return sign

def header(session):
    sign = signer(session)

    return f"<a href='{sign('/logout')}'>Logout</a> <a href='/view'>My Mokers</a> <a href='/add'>Add a Moker</a> <a href='/create'>Create a new Moker</a> <a href='/delete'>Remove Moker</a>\
<form id='add' method='POST' action='{sign('/add?daily=1')}'><input type='submit' value='*Add \"Moker of the Day\"*'/></form>"

########### ROUTES

@app.route("/")
def home():
    session = request.cookies.get("session", None)
    if session is None or session not in sessions:
        return "<!DOCTYPE html><html><body>Welcome to my Moker Collection website. Please <a href=/register>register</a> or <a href=/login>login</a>.</body></html>"
    
    return redirect("/view")

@app.route('/static/<path:path>')
def staticServe(path):
    return send_from_directory('static', path)

@app.route("/register", methods=["GET"])
def register_form():
    return "<!DOCTYPE html><html><body>Register an Account<br>\
<form method='POST'><input type='text' name='user' value='username'><input type='text' name='password' value='password (stored in plaintext for you)'><input type='submit' value='Submit'></form></body></html>"

@app.route("/register", methods=["POST"])
def register():
    user = request.form.get("user", None)
    password = request.form.get("password", None)
    if user is None or password is None:
        return "Need user and password"
    if not (MOKER_PATTERN.match(user) and MOKER_PATTERN.match(password)):
        return "Invalid username/password"
    users[user] = {"password": password, "mokers": []}
    return redirect("/login")

@app.route("/login", methods=["GET"])
def login_form():
    return "<!DOCTYPE html><html><body>Login<br>\
<form method='POST'><input type='text' name='user' value='Username'><input type='text' name='password' value='password (stored in plaintext for you)'><input type='submit' value='Submit'></form></body></html>"

@app.route("/login", methods=["POST"])
def login():
    user = request.form.get("user", "")
    password = request.form.get("password", "")
    if user not in users:
        return "No user"
    if users[user]["password"] == password:
        response = make_response(redirect("/view"))
        sid = request.cookies.get("session", secrets.token_hex(16))
        sessions[sid].clear()
        response.set_cookie("session", sid, httponly=True)
        sessions[sid]["user"] = user
        sessions[sid]["key"] = secrets.token_bytes(16)
        return response
    return "Invalid user/pass"

@app.route("/logout", methods=["GET"])
@csrf
def logout():
    sid = request.cookies.get("session") # already exists given by @csrf
    del sessions[sid]
    r = make_response(redirect("/"))
    r.delete_cookie("session")
    return r

@app.route("/view", methods=["GET"])
@session
def view(session):
    style = request.args.get("style", "/static/plain.css")
    if not STYLE_PATTERN.match(style):
        return "Bad style link"

    mokers = "<br>".join(f"<img src={imgur(moker)} referrerpolicy=no-referrer class=moker></img>" for moker in users[session["user"]]["mokers"])
    styles = " ".join(f"<a href=/view?style=/static/{s}>{s}</a>" for s in STYLES)
    return f"<!DOCTYPE html><html><head><link rel=stylesheet href={style}></head><body>{header(session)}<br>Use Some Styles: {styles}<br>Your'e Mokers: <br><br>{mokers}</body></html>"

@app.route("/create", methods=["GET"])
@session
def create_form(session):
    sign = signer(session)
    form = f"<form action='/create' method='POST'><input type='text' name='name' value='Name of Moker'><input type='text' name='path' value='imgur path without extension'><input type='submit' value='Create'></form>"

    return "<!DOCTYPE html><html><body>" + header(session) + "Create a moker.<br>" + form + "</body></html>"

@app.route("/create", methods=["POST"])
@session
def create(session):
    if len(MOKERS) > 30:
        return "We are at max moker capacity. Safety protocols do not allow adding more moker"

    name = request.form.get("name", None)
    if name is None or name in MOKERS:
        return "No name for new moker"
    path = request.form.get("path", None)
    if path is None or not MOKER_PATTERN.match(path):
        return "Invalid moker path"

    if requests.get(imgur(path)).status_code != 200:
        return "This moker does not appear to be valid"
    
    MOKERS[name] = path
    return redirect("/view")

@app.route("/add", methods=["GET"])
@session
def add_form(session):
    sign = signer(session)
    mokers = " ".join(f"<form action='{sign('/add?moker=' + moker)}' method='POST'><input type='submit' value='{moker}'></form>" for moker in MOKERS)
    return "<!DOCTYPE html><html><body>" + header(session) + "Add a moker to your list.<br>" + mokers + "</body></html>"

@app.route("/add", methods=["POST"])
@csrf
@session
def add(session):
    moker = request.args.get("moker", None)
    if moker is None:
        if request.args.get('daily', False):
            moker = MOKEROFTHEDAY
    if (moker == "flagmoker" and session["user"] != "@admin") or moker not in MOKERS:
        return "Invalid moker"

    if requests.get(imgur(MOKERS[moker])).status_code != 200:
        return "This moker is not avaliable at this time"

    if(len(users[session["user"]]["mokers"]) > 30):
        # this is too many mokers for one person. you don't need this many
        users[session["user"]]["mokers"].clear()
    users[session["user"]]["mokers"].append(MOKERS[moker])
    return redirect("/view")

@app.route("/delete", methods=["GET"])
@session
def delete_form(session):
    sign = signer(session)
    mokers = " ".join(f"<form action={sign('/delete?moker=' + moker)} method=POST><img src={imgur(moker)}></img><input type=submit value=Remove></form>" for moker in users[session["user"]]["mokers"])
    return "<!DOCTYPE html><html><body>" + header(session) + "Remove a moker from your list.<br>" + mokers + "</body></html>"

@app.route("/delete", methods=["POST"])
@csrf
@session
def delete(session):
    moker = request.args.get("moker", None)
    if moker is None:
        return "No moker to remove"
    users[session["user"]]["mokers"].remove(moker)
    return redirect("/view")
