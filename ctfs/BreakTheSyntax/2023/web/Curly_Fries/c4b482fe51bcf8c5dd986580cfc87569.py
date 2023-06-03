import datetime
import functools
import random
import subprocess
from urllib.parse import quote_plus, urlencode

from .db import get_tasks, get_user, register_user
from flask import redirect, render_template, request, url_for, Blueprint
from flask_jwt_extended import create_access_token, jwt_required
from flask_jwt_extended.exceptions import NoAuthorizationError

from . import jwt

"""
Challenge description: 
Welcome to Curly Fries Restaurant! We love our fries curly and we hope you will too. Just place your order, sit back,
relax and watch as our team runs around the kitchen to quickly deliver your meal!
"""

bp = Blueprint("app_1", __name__)


def localhost_only(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.remote_addr != "127.0.0.1":
            return render_template(
                "info.html", info="This page can only be accessed locally!"
            )
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/")
def index():
    return render_template("index.html")


# Reports say some customers tried to smuggle something extra in their order ...
@bp.route("/order", methods=["POST"])
def order():
    form = request.form
    params = [k + "=" + v for k, v in form.items()]
    command = "curl -X POST http://127.0.0.1:1337/kitchen -d " + "&".join(params)
    try:
        return subprocess.check_output(command.split(" "))
    except:
        return render_template(
            "info.html", info="Oops ... there was a problem processing your order :("
        )


@bp.route("/kitchen", methods=["POST"])
@localhost_only
def kitchen():
    order_items = ", ".join([k + ": " + v for k, v in request.form.items()])
    order_id = random.randint(13, 37)
    order_time = (
        datetime.datetime.now() + datetime.timedelta(minutes=random.randint(5, 10))
    ).strftime("%H:%M")
    return render_template(
        "info.html",
        info="Your order has been placed!",
        items=order_items,
        id=order_id,
        time=order_time,
    )


@bp.route("/register", methods=["GET", "POST"])
@localhost_only
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if register_user(username, password):
            return render_template(
                "info.html",
                info="Success! Thank you for registering at Curly Fries Restaurant.",
            )
        else:
            return render_template("info.html", info="This user already exists!")
    return render_template("register.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user(username, password)
        if user:
            token = create_access_token(identity=username)
            resp = redirect(url_for("dashboard"))
            resp.set_cookie("access_token_cookie", token)
            return resp
        else:
            return render_template("info.html", info="Invalid credentials!")
    return render_template("login.html")


@bp.route("/dashboard")
@jwt_required()
def dashboard():
    tasks = get_tasks()
    return render_template("dashboard.html", tasks=tasks)


# JWT error handling
@jwt.unauthorized_loader
def handle_unauthorized(error):
    if isinstance(error, NoAuthorizationError):
        return render_template("info.html", info="Missing access token cookie"), 401
    else:
        return render_template("info.html", info="Unauthorized"), 401
