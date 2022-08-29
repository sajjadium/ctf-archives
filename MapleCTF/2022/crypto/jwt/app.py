from flask import Flask, request, render_template, flash, url_for, redirect, g
from flask_cors import CORS
from models import User, db
from secret import flag
from jwt import jwt
import os


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/jwt.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config["SECRET_KEY"] = os.urandom(32).hex()

    db.init_app(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(username="admin", password=os.urandom(32).hex())
        db.session.add(user)
        db.session.commit()

    return app


app = create_app()


@app.route("/")
def index():
    return redirect("login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        error = None
        if not username or not password:
            error = "Missing username or password"

        if User.query.filter(User.username == username).first() is not None:
            error = "User already exists"

        if not error:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))

        flash(error)

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter(
            User.username == username, User.password == password
        ).one_or_none()

        if user:
            token = jwt.sign({"user": username})
            resp = redirect(url_for("home"))
            resp.set_cookie("token", token)
            return resp

        flash("Invalid username or password")

    return render_template("login.html")


@app.before_request
def load_user():
    if not (token := request.cookies.get("token")):
        return

    try:
        user = jwt.decode(token)["user"]
        g.user = user

    except Exception as e:
        return


@app.route("/logout", methods=["GET", "POST"])
def logout():
    if hasattr(g, "user"):
        resp = redirect(url_for("login"))
        resp.set_cookie("token", "", expires=0)
        return resp

    return redirect(url_for("login"))


@app.route("/home", methods=["GET"])
def home():
    if hasattr(g, "user"):
        if g.user == "admin":
            message = f"Welcome back! Here's your flag {flag}"
        else:
            message = f"Welcome back {g.user}!"
        return render_template("home.html", message=message)

    flash("An error occurred - please login again")
    return redirect(url_for("login"))
