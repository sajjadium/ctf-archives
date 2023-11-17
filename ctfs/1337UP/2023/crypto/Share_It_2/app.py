from flask import Flask, render_template, request, redirect, url_for, make_response
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import json
import base64
from uuid import uuid4
import time
from waitress import serve

app = Flask(__name__)

key = os.urandom(16)

id_to_iv = {}
last_clear = int(time.time())

FLAG = os.getenv("FLAG")
if not FLAG:
    FLAG = "FLAG{dummy}"


def store_iv(iv):
    # Clear dict once every hour
    global last_clear
    crnt_time = time.time()
    if crnt_time > 1*60*60 + last_clear:
        id_to_iv.clear()
        last_clear = crnt_time
    iv_id = str(uuid4())
    id_to_iv[iv_id] = iv
    return iv_id


def gen_encrypted_cookie(username, first_name, last_name):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    user_dict = {'username': username, 'first_name': first_name,
                 'last_name': last_name, 'admin': False}
    c = cipher.encrypt(pad(json.dumps(user_dict).encode(), 16))
    iv_id = store_iv(iv)
    return base64.b64encode(json.dumps({'user_dict': base64.b64encode(c).decode(),
                                        'id': iv_id}).encode()).decode()


def decrypt_cookie(cookie, iv=None):
    cookie_dict = json.loads(base64.b64decode(cookie).decode())
    if iv:
        iv = bytes.fromhex(iv)
    else:
        iv_id = cookie_dict['id']
        iv = id_to_iv.get(iv_id)
        if not iv:
            raise Exception(f'IV not found using id: {iv_id}')
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    try:
        pt = cipher.decrypt(base64.b64decode(
            cookie_dict['user_dict'].encode()))
    except:
        raise Exception("Decryption error")
    try:
        pt = unpad(pt, 16)
    except:
        raise Exception("Unpad error")
    try:
        user_dict = json.loads(pt)
    except:
        raise Exception(f'Invalid json: {pt}')
    return user_dict


@app.route("/")
def index():
    cookie = request.cookies.get("token")
    if cookie == None:
        return redirect(url_for('register'))
    else:
        try:
            user_dict = decrypt_cookie(cookie, iv=request.args.get("debug_iv"))
        except Exception as e:
            return str(e), 500
        return render_template('index.html', username=user_dict['username'])


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form["username"]
        print(f'{username=}')
        if username == None or username == "":
            return "username must be set", 400
        first_name = request.form["first_name"]
        if first_name == None or first_name == "":
            return "first_name must be set", 400
        last_name = request.form["last_name"]
        if last_name == None or last_name == "":
            return "last_name must be set", 400
        cookie = gen_encrypted_cookie(username, first_name, last_name)
        res = make_response(redirect(url_for('index')))
        print(cookie)
        res.set_cookie('token', cookie)
        return res


@app.route("/admin-opinions")
def admin():
    cookie = request.cookies.get("token")
    if cookie == None:
        return redirect(url_for('register'))
    else:
        try:
            user_dict = decrypt_cookie(cookie, iv=request.args.get("debug_iv"))
        except Exception as e:
            return str(e), 500
        if not user_dict['admin'] == True:
            return "<p>Only admins are allowed to read these cool opionons</p>", 403
        else:
            return render_template("admin.html", flag=FLAG)


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port='5000')
