from flask import Flask, render_template, request, redirect, make_response
from json import loads, dumps
import secrets
import random
import math
import time
import binascii
import sys
from Crypto.Cipher import AES 
from Crypto.Hash import SHA
from Crypto.Util.Padding import pad, unpad

sys.tracebacklimit = 0

app = Flask(__name__)

with open("flag.txt", "r") as file:
    flag = file.read()

with open("key.txt", "r") as f:
    key = SHA.new(int(f.read().strip()).to_bytes(64, 'big')).digest()[0:16]

def encrypt(msg: str):
    iv = secrets.token_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(msg.encode('utf-8'), 16))
    iv_enc = AES.new(key[3:] + b'tmp', AES.MODE_ECB).encrypt(iv)
    return binascii.hexlify(iv_enc + ct).decode("ascii")

def decrypt(token: str):
    ive = binascii.unhexlify(token[:32])
    ct = binascii.unhexlify(token[32:])
    iv = AES.new(key[3:] + b'tmp', AES.MODE_ECB).decrypt(ive)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ct), 16).decode("ascii", errors='ignore')

def check_token(token: str):
    contents = decrypt(token)
    try:
        return loads(contents)
    except:
        return None

@app.route("/")
def home():
    user = None
    token = request.cookies.get("enterprise-grade-token")
    if token is not None:
        user = check_token(token)
        if user is None:
            return render_template("flagmachine.html", message="At Generic Enterprise™, We have Standards™. That's why we require all input Data™ to be strictly valid JSON.", hidebutton=True), 400
        return render_template("home.html", username=user["name"], is_admin=user["admin"])
    else:
        return render_template("home.html")

@app.route("/login")
def login():
    contents = dumps({"name": "Enterprise Vampire", "admin": False})
    token = encrypt(contents)
    response = redirect("/", code=303)
    response.set_cookie("enterprise-grade-token", token)
    return response

@app.route("/logout")
def logout():
    response = redirect("/", code=303)
    response.delete_cookie("enterprise-grade-token")
    return response

@app.route("/flagmachine/on")
def turn_flagmachine_on():
    token = request.cookies.get("enterprise-grade-token")
    if token is None:
        return render_template("flagmachine.html", message="At Generic Enterprise™, We Care about Security and Privacy. That's why we require you to Authenticate™ first before modifying any Enterprise™ Industrial™-Grade Settings™."), 401
    user = check_token(token)
    if user is None:
        return render_template("flagmachine.html", message="At Generic Enterprise™, We have Standards™. That's why we require all input Data™ to be strictly valid JSON."), 400
    if user["admin"]:
        return render_template("flagmachine.html", message=flag)
    else:
        return render_template("flagmachine.html", message="At Generic Enterprise™, We Care about Security and Privacy. That's why only Authorized™ Personnel™ are permitted to modify our Enterprise™ Industrial™-Grade Settings™."), 403
