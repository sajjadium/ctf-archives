import secrets
from flask import Flask, render_template, request
import pickle
import base64

flag = "REDACTED"

app = Flask(__name__)

users = {
    "example-user": {
        "name": "example",
        "bio": "this is example"
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new", methods=["POST"])
def new():
    pickle_str = base64.b64decode(request.get_data())
    
    if len(pickle_str) > 138:
        return "uhoh"

    dict_prefix = b"\x80\x04\x95" + chr(len(pickle_str)-11).encode() + b"\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x04name\x94\x8c"
    dict_suffix = b"\x94u."
    
    # make sure dictionary is valid and no funny business is going on
    if pickle_str[:len(dict_prefix)] != dict_prefix or pickle_str[-len(dict_suffix):] != dict_suffix or b"flag" in pickle_str or b"os." in pickle_str or b"open" in pickle_str:
        return "uhoh"

    url = secrets.token_urlsafe(16)
    obj = pickle.loads(pickle_str)
    users[url] = obj

    return "user?id=" + url

@app.route("/uhoh")
def uhoh():
    return render_template("uhoh.html")

@app.route("/user", methods=["GET"])
def user():
    uid = request.args.get("id")
    if len(uid) < 10:
        return "id too short"
    if uid not in users:
        return "user not found :("
    return render_template("user.html", user=users[uid])
