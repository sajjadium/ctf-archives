from flask import Flask, render_template, request, redirect, url_for, make_response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import json
import base64
from waitress import serve

app = Flask(__name__)

key = os.urandom(16)

FLAG = os.getenv("FLAG")
if not FLAG:
    FLAG = "FLAG{dummy}"


def gen_encrypted_cookie(username):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    user_dict = {'admin': False, 'username': username}
    c = cipher.encrypt(pad(json.dumps(user_dict).encode(), 16))
    return base64.b64encode(json.dumps({'user_dict': base64.b64encode(c).decode(),
                                        'iv': base64.b64encode(iv).decode()}).encode()).decode()


def decrypt_cookie(cookie):
    cookie_dict = json.loads(base64.b64decode(cookie).decode())
    iv = base64.b64decode(cookie_dict['iv'].encode())
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return json.loads(unpad(cipher.decrypt(base64.b64decode(cookie_dict['user_dict'].encode())), 16))


@app.route("/")
def index():
    cookie = request.cookies.get("token")
    if cookie == None:
        return redirect(url_for('register'))
    else:
        try:
            user_dict = decrypt_cookie(cookie)
        except:
            return redirect(url_for('register'))
        return render_template('index.html', username=user_dict['username'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        if username == None or username == "":
            return "username must be set", 400
        cookie = gen_encrypted_cookie(username)
        res = make_response(redirect(url_for('index')))
        res.set_cookie('token', cookie)
        return res


@app.route("/admin-opinions")
def admin():
    cookie = request.cookies.get("token")
    if cookie == None:
        return redirect(url_for('register'))
    else:
        try:
            user_dict = decrypt_cookie(cookie)
        except:
            return redirect(url_for('register'))
        if not user_dict['admin'] == True:
            return "<p>Only admins are allowed to read these cool opionons</p>", 403
        else:
            return render_template("admin.html", flag=FLAG)


if __name__ == '__main__':
    print("Starting app...")
    serve(app, host='0.0.0.0', port='5000')
