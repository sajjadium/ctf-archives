from flask import Flask, session, render_template, request, redirect, make_response
from secret import secret, flag, firstSecret, secondSecret
from db import db
import os
from hashlib import sha1
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)


## INSTANCER CODE

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == os.getenv('INSTANCER_USERNAME'):
        return os.getenv('INSTANCER_PASSWORD')
    return None

## END OF INSTANCER CODE


app.secret_key = secret


def createSession(user):
    session["loggedIn"] = True
    session["user"] = {}
    session["user"]["id"] = user[0]
    session["user"]["name"] = user[1]
    session["user"]["isAdmin"] = user[2] is True


def signFile(data):
    data = data + bytes([session["user"]["id"]])
    signature = sha1(bytes(str(firstSecret), "utf-8") + data).digest()
    signature = sha1(bytes(str(secondSecret), "utf-8") + signature).digest()

    return data + signature

def verifySignature(data):
    signedData = data[:-20]
    fileSignature = data[-20:]
    userId = signedData[-1]

    calculatedSignature = sha1(bytes(str(firstSecret), "utf-8") + signedData).digest()
    calculatedSignature = sha1(bytes(str(secondSecret), "utf-8") + calculatedSignature).digest()

    if fileSignature == calculatedSignature:
        return userId
    else:
        raise "Invalid Signature"


@app.route("/flag")
@auth.login_required # < INSTANCER CODE
def flagEndpoint():
    if "loggedIn" in session and session["user"]["isAdmin"]:
        return flag
    else:
        return "Only admin has access to flag !"


@app.route("/")
@auth.login_required # < INSTANCER CODE
def index():
    if "loggedIn" in session:
        return redirect("home")
    return render_template("index.html")


@app.route("/home")
@auth.login_required # < INSTANCER CODE
def home():
    return render_template("home.html", user=session["user"])


@app.route("/register", methods=['GET', 'POST'])
@auth.login_required # < INSTANCER CODE
def register():
    if request.method == "POST":
        if type(request.form["username"]) != str or type(request.form["password"]) != str:
            return render_template("register.html")
        try:
            cursor = db.cursor()
            results = cursor.execute(f'''
                INSERT INTO users (name, password, isAdmin) VALUES ( '{request.form["username"]}', '{request.form["password"]}', 0); 
                SELECT id, name, isAdmin FROM users ORDER BY id DESC LIMIT 1;
                ''', 
            multi=True)

            user = ()
            for cur in results:
                user = cur.fetchone()
            db.commit()

            createSession(user)
        except Exception as a:
            return render_template("register.html", message="User already registered")

        return redirect("/home")
    
    return render_template("register.html")


@app.route("/login", methods=['GET', 'POST'])
@auth.login_required # < INSTANCER CODE
def login():
    if request.method == "POST":
        if type(request.form["username"]) != str or type(request.form["password"]) != str:
            return render_template("login.html")
        
        cursor = db.cursor()
        cursor.execute('SELECT id, name, isAdmin FROM users WHERE name = %(username)s AND password = %(password)s', 
            {
                "username": request.form["username"],
                "password": request.form["password"]
            }
        )
        users = cursor.fetchall()

        if len(users) > 0:
            createSession(users[0])
            return redirect("/home")
        else:
            return render_template("login.html", message="Wrong username or password")

    return render_template("login.html")


@app.route("/sign", methods=['GET', 'POST'])
@auth.login_required # < INSTANCER CODE
def sign():
    if not "loggedIn" in session:
        return redirect("/")
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("sign.html", message="No file")
        
        file = request.files['file']
        data = file.read()
        response = make_response(signFile(data))
        response.headers.set('Content-Type', 'application/octet-stream')
        response.headers.set('Content-Disposition', 'attachment', filename=request.files['file'].name)
        return response

    return render_template("sign.html", user=session["user"])


@app.route("/verify", methods=['GET', 'POST'])
@auth.login_required # < INSTANCER CODE
def verify():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template("verify.html", message="No file")
        try: 
            file = request.files['file']
            data = file.read()
            userId = verifySignature(data)
            cursor = db.cursor()
            cursor.execute(f"SELECT name from users where id = {userId}")
            username = cursor.fetchone()[0]
            return render_template("verify.html", message="Valid signature, file signed by: %s" % username)
        except:
            return render_template("verify.html", message="Invalid signature!")

    return render_template("verify.html")

