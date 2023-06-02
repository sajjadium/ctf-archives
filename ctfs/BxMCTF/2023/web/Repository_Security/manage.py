import json
import os
from functools import wraps

import click
from flask import Flask, jsonify, render_template
from flask_simplelogin import Message, SimpleLogin, login_required
from werkzeug.security import check_password_hash, generate_password_hash


# [ -- Utils -- ]


def validate_login(user):
    db_users = json.load(open("users.json"))
    if not db_users.get(user["username"]):
        return False
    stored_password = db_users[user["username"]]["password"]
    if check_password_hash(stored_password, user["password"]):
        return True
    return False


def create_user(**data):
    """Creates user with encrypted password"""
    if "username" not in data or "password" not in data:
        raise ValueError("username and password are required.")

    # Hash the user password
    data["password"] = generate_password_hash(
        data.pop("password"), method="pbkdf2:sha256"
    )

    # Here you insert the `data` in your users database
    # for this simple example we are recording in a json file
    db_users = json.load(open("users.json"))
    # add the new created user to json
    db_users[data["username"]] = data
    # commit changes to database
    json.dump(db_users, open("users.json", "w"))
    return data


# [--- Flask Factories  ---]


def create_app():
    app = Flask(__name__)
    app.config.from_object("settings")
    return app


def configure_extensions(app):
    messages = {
        "login_success": "Welcome!",
        "is_logged_in": Message("already logged in", "success"),
        "logout": None,
    }
    SimpleLogin(app, login_checker=validate_login, messages=messages)
    if not os.path.exists("users.json"):
        with open("users.json", "a") as json_file:
            # This just touch create a new dbfile
            json.dump({"username": "", "password": ""}, json_file)


def configure_views(app):
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/secret")
    @login_required()
    def secret():
        return render_template("secret.html")

    @app.route("/api", methods=["POST"])
    @login_required(basic=True)
    def api():
        return jsonify(data="You are logged in with basic auth")

    @app.route("/complex")
    @login_required(username=["admin"])
    def complexview():
        return render_template("secret.html")


# [--- Command line functions ---]


def with_app(f):
    """Calls function passing app as first argument"""

    @wraps(f)
    def decorator(*args, **kwargs):
        app = create_app()
        configure_extensions(app)
        configure_views(app)
        return f(app=app, *args, **kwargs)

    return decorator


@click.group()
def main():
    """Flask Simple Login Example App"""


@main.command()
@click.option("--username", required=True, prompt=True)
@click.option(
    "--password", required=True, prompt=True, hide_input=True, confirmation_prompt=True
)
@with_app
def adduser(app, username, password):
    """Add new user with admin access"""
    with app.app_context():
        create_user(username=username, password=password)
        click.echo("user created!")


@main.command()
@click.option("--reloader/--no-reloader", default=None)
@click.option("--debug/--no-debug", default=None)
@click.option("--host", default=None)
@click.option("--port", default=None)
@with_app
def runserver(app=None, reloader=None, debug=None, host=None, port=None):
    """Run the Flask development server i.e. app.run()"""
    debug = debug or app.config.get("DEBUG", False)
    reloader = reloader or app.config.get("RELOADER", False)
    host = host or app.config.get("HOST", "127.0.0.1")
    port = port or app.config.get("PORT", 5000)
    app.run(use_reloader=reloader, debug=debug, host=host, port=port)


# [--- Entry point ---]

if __name__ == "__main__":
    # python manage.py to see help
    main()
