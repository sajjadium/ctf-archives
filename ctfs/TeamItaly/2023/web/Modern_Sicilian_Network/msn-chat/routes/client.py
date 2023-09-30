import os
from flask import Blueprint, session, redirect, render_template
from utils.models import *

DOMAIN = os.getenv("DOMAIN")
SPACES_PORT = os.getenv("SPACES_PORT")

bp = Blueprint("client", __name__)

@bp.route("/")
def index():
    return redirect("/login")

@bp.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("propic", None)
    return redirect("/")

@bp.route("/login")
def login():
    if "id" in session:
        return redirect("/chat")
    return render_template("login.html", propics=ALLOWED_PROPICS)

@bp.route("/chat/")
@bp.route("/chat/<uuid>")
def client(uuid=None):
    if uuid is None:
        uuid = User.query.filter_by(username="Loldemort").first().id
        return redirect(f"/chat/{uuid}")
    if "id" not in session:
        return redirect("/login")
    return render_template("chat.html", DOMAIN=DOMAIN, SPACES_PORT=SPACES_PORT)