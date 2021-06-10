from flask import (
    Flask,
    render_template,
    render_template_string,
    request,
    redirect,
    make_response,
    session,
    jsonify,
    url_for,
    g,
)
from functools import wraps
from sqlalchemy import or_
from backend.models import db, User
import os

template_dir = os.path.abspath(".")
app = Flask(__name__, template_folder=template_dir)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///DB/db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "<REDACTED>"
app.config["SESSION_COOKIE_NAME"] = "auth"
app.jinja_env.globals.update(environ=os.environ.get)


@app.before_first_request
def create_tables():
    db.create_all()

    try:
        user = User(
            username=os.environ.get("ADMIN_BOT_USER"),
            email="admin@admin.com",
            password=os.environ.get("ADMIN_BOT_PASSWORD"),
            about="",
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(str(e), flush=True)


db.init_app(app)


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        sessionID = session.get("id", None)
        if not sessionID:
            return redirect(url_for("signin", error="Invalid session please sign in"))

        g.user = User.query.get(sessionID)
        return f(*args, **kwargs)

    return wrap


def logged_should_not_visit(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        sessionID = session.get("id", None)
        if sessionID:
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return wrap


@app.route("/signup", methods=["GET", "POST"])
@logged_should_not_visit
def signup():

    if request.method == "GET":
        return render_template("backend/default_templates/signup.html")

    elif request.method == "POST":
        data = request.get_json(force=True)

        username = data.get("username", None)
        email = data.get("email", None)
        password = data.get("password", None)
        password2 = data.get("password2", None)

        if not username or not email or not password or not password2:
            response = make_response(
                jsonify({"message": "Missing parameters"}),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        # Check if user or email exists
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if user:
            response = make_response(
                jsonify(
                    {
                        "message": "This username and/or email is already taken please choose another one"
                    }
                ),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        # Check if passwords match
        if password != password2:
            response = make_response(
                jsonify({"message": "Passwords do not match"}),
                400,
            )
            response.headers["Content-Type"] = "application/json"
            return response

        user = User(username=username, email=email, password=password, about="")
        db.session.add(user)
        db.session.commit()

        response = make_response(
            jsonify({"message": "Successfully signed up."}),
            200,
        )
        response.headers["Content-Type"] = "application/json"
        return response


@app.route("/signin", methods=["GET", "POST"])
@logged_should_not_visit
def signin():

    if request.method == "GET":
        success = request.args.get("success", None)
        error = request.args.get("error", None)

        return render_template(
            "backend/default_templates/signin.html", success=success, error=error
        )

    elif request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if user exists
        user = User.query.filter(
            User.username == username, User.password == password
        ).first()
        if not user:
            return redirect(url_for("signin", error="Invalid credentials"))

        session["id"] = user.id
        return redirect(url_for("home"))


@app.route("/logout")
@login_required
def logout():
    session.pop("id", None)
    return redirect(url_for("signin", success="Logged out successfully."))
