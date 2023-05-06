from flask import Flask, request
from flask_httpauth import HTTPBasicAuth
import os

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {'admin': os.environ.get('SECRET')}


@auth.verify_password
def verify_password(username, password):
    if username in users and password == users.get(username):
        return username


@app.route('/')
@auth.login_required
def index():
    if request.headers.get("TOKEN") == os.environ.get("TOKEN"):
        return os.environ.get("FLAG")

    return "Flag is only available through our Chrome extension."


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get("Origin")
    response.headers['Access-Control-Allow-Headers'] = 'Token, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response
