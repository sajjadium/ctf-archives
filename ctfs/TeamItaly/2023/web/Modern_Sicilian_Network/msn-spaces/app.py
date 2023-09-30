import os
import uuid
from datetime import datetime
from time import sleep
from flask import Flask, render_template
from utils.models import *

SECRET_KEY = os.getenv("SECRET_KEY")
DOMAIN = os.getenv("DOMAIN")
CHAT_PORT = os.getenv("CHAT_PORT")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_COOKIE_DOMAIN"] = f".{DOMAIN}"

from utils.db import db
db.init_app(app)

@app.after_request
def csp(r):
    r.headers["Content-Security-Policy"] = f"default-src 'self' 'unsafe-inline' chat.{DOMAIN}:{CHAT_PORT}"
    r.headers["Access-Control-Allow-Origin"] = "*"
    return r

from routes import api
app.register_blueprint(api.bp)

from routes import pages
app.register_blueprint(pages.bp)