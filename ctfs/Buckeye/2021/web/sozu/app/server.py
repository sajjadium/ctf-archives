from flask import Flask, request, abort, Response, jsonify, Blueprint, render_template
import os

app = Flask(__name__)

internal = Blueprint('internal', __name__)
public = Blueprint('public', __name__)


@internal.route('/')
def internal_home():
    return render_template("internal/home.html")

@internal.route('/flag')
def internal_flag():
    return jsonify({"flag": os.getenv("FLAG")})

@public.route('/')
def public_home():
    return render_template("public/home.html")

app.register_blueprint(internal, url_prefix="/internal")
app.register_blueprint(public, url_prefix="/public")
