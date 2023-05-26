from flask import Flask, request, render_template, redirect, make_response
from base64 import b64encode, b64decode
import hashlib
import random
import json

app = Flask(__name__)
users = {}


def hash(data):
    return hashlib.sha256(bytes(data, 'utf-8')).hexdigest()


@app.route('/')
def index():
    if request.cookies.get('data') is None or request.cookies.get('hash') is None:
        return redirect('/login')

    data = request.cookies.get('data')
    decoded = b64decode(data)
    data_hash = request.cookies.get('hash')
    payload = json.loads(decoded)

    if payload['username'] not in users:
        resp = make_response(redirect('/login'))
        resp.set_cookie('data', '', expires=0)
        resp.set_cookie('hash', '', expires=0)
        return resp

    actual_hash = hash(data + users[payload['username']])

    if data_hash != actual_hash:
        return redirect('/login')

    if payload['user_type'] == 'premium':
        theme_name = request.args.get('theme') or 'static/premium.css'
        return render_template('premium.jinja', theme_to_use=open(theme_name).read())
    else:
        return render_template('basic.jinja')


@app.route('/login', methods=['GET'])
def get_login():
    return render_template('login.jinja')


@app.route('/login', methods=['POST'])
def post_login():
    username = request.form['username']

    if username not in users:
        users[username] = hex(random.getrandbits(24))[2:]

    resp = make_response(redirect('/'))
    data = {
        "username": username,
        "user_type": "basic"
    }

    b64data = b64encode(json.dumps(data).encode())
    data_hash = hash(b64data.decode() + users[username])
    resp.set_cookie('data', b64data)
    resp.set_cookie('hash', data_hash)
    return resp


if __name__ == '__main__':
    app.run()
