import ast
import string
import random
from hashlib import sha1

from flask import render_template, request, flash, make_response
from app import app

letters = string.ascii_letters
secret = ''.join(random.choice(letters) for i in range(random.randint(15,35)))

def new_user():
    user = "admin=False"
    data = secret + user
    mac = sha1(data.encode()).hexdigest()
    cookie_val = user.encode().hex() + "." + mac
    return cookie_val


def validate(cookie):
    user_hex = cookie.split(".")[0]
    user = bytes.fromhex(user_hex)
    data = secret.encode() + user
    
    cookie_mac = cookie.split(".")[1]
    if cookie_mac != sha1(data).hexdigest():
        raise Exception("MAC does not match!")
    
    return ast.literal_eval(user.split(b"=")[-1].decode())
    

@app.route("/", methods=["GET"])
def base():
    if not request.cookies.get('auth'):
        resp = make_response(render_template('index.html'))
        resp.set_cookie('auth', new_user())
        return resp
    else:
        try:
            admin = validate(request.cookies.get('auth'))
        except Exception as e:
            flash(str(e), 'danger')
            return render_template('index.html')

        if admin:
            return render_template('admin.html')
        else:
            return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', threaded=True)