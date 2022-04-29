import string
import random
from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

from flask import render_template, request, make_response, redirect
from app import app, confidential_settings, admin


BS = AES.block_size
IV = get_random_bytes(BS)
KEY = get_random_bytes(BS)
BLUE = "#076185"
RAND = ''.join(random.choice(string.ascii_letters) for i in range(BS))


def make_cookie(color):
    cookie = f"color:{color}|{RAND}"
    cookie += confidential_settings
    return encrypt_cookie(cookie)


def encrypt_cookie(cookie: str) -> bytes:
    raw = pad(cookie.encode(), BS)
    cipher = AES.new(KEY, AES.MODE_CBC, IV).encrypt(raw)
    return b64encode(cipher)


def decrypt_cookie(cookie: bytes) -> bytes:
    cipher = b64decode(cookie)
    raw = AES.new(KEY, AES.MODE_CBC, IV).decrypt(cipher)
    return unpad(raw, BS)
    

@app.route("/", methods=["GET", "POST"])
def base():
    if request.method == "GET":
        if not request.cookies.get('session'):
            resp = make_response(render_template('index.html', color=BLUE))
            resp.set_cookie('session', make_cookie(BLUE))
            return resp
        else:
            cookie: bytes = decrypt_cookie(request.cookies.get('session'))
            color: string = cookie[6:13].decode()
            if admin(cookie) == True:
                return render_template('admin.html', color=color)
            else:
                return render_template('index.html', color=color)
    else:
        if request.form['color']:
            resp = make_response(redirect('/'))
            resp.set_cookie('session', make_cookie(request.form['color']))
            return resp
        else:
            return redirect("/")
        

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', threaded=True)