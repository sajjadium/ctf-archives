from flask import Flask, request, redirect, session, render_template, jsonify, g
from flask_cors import CORS
from subprocess import run
from os import urandom
from re import match
import sqlite3

# Init
secret = urandom(32)
app = Flask(__name__)
# app.config["DEBUG"] = True
app.config["SECRET_KEY"] = secret
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "None"
cors = CORS(app, resources={
    r"/api/*": {
        "origins": ["null"]
    }
}, allow_headers=[
    "Authorization",
    "Content-Type"
], supports_credentials=True)


# Database
db_file = "sqlite.db"

def connect_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_file)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# Handle 404 pages
@app.errorhandler(404)
def page_not_found(error):
    if "logged" in session:
        return redirect("/notes")
    else:
        return redirect("/login", 302)


# API routes
import api


# Routes
@app.route("/login", methods=["GET"])
def login():
    if "logged" in session:
        return redirect("/notes")

    return render_template("login.html", title="Login")


@app.route("/register", methods=["GET"])
def register():
    if "logged" in session:
        return redirect("/notes")

    return render_template("register.html", title="Register")


@app.route("/notes", methods=["GET"])
def notes():
    if not "logged" in session:
        return redirect("/login")

    return render_template("notes.html", username=session["username"], title="Notes")


@app.route("/notes/create", methods=["GET"])
def create():
    if not "logged" in session:
        return redirect("/login")

    return render_template("create.html", username=session["username"], title="Create note")


@app.route("/note/<string:uuid>", methods=["GET"])
def view(uuid):
    if not "logged" in session:
        return redirect("/login")

    return render_template("edit.html", username=session["username"], uuid=uuid, title="Edit note")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    r = request.args.get("r") if request.args.get("r") else "/login"
    return redirect(r)


@app.route("/report", methods=["POST"])
def report():
    url = request.form.get("url")
    if not match("^http(s)?://.*", url):
        return jsonify({"error": "The URL must match ^http(?)://.* !"})

    else:
        run(["node", "/usr/app/bot/bot.js", url])
        return jsonify({"success": "Your request has been sent to an administrator!"})


# Start
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, ssl_context=("/usr/app/cert/cert.pem", "/usr/app/cert/key.pem"))
