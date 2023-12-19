from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())


@app.route("/login", methods=["POST", "GET"])
def login():
    if "logged_in" in session and session["logged_in"]:
        session.pop("logged_in", None)
        return redirect(url_for("login"))

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        loweruser = username.lower()
        lowerpass = password.lower()
        invalid_entries = invalid_entries = [
            "=",
            "<",
            ">",
            "+",
            "//",
            "|",
            ";",
            " ",
            " ",
            "'1",
            " 1",
            " true",
            "'true",
            " or",
            "'or",
            "/or",
            " and",
            "'and",
            "/and",
            "'like",
            " like",
            "/like",
            "'where",
            " where",
            "/where",
            "%00",
            "null",
            "admin'",
        ]
        matching_value = next(
            (
                value
                for value in invalid_entries
                if value in loweruser or value in lowerpass
            ),
            None,
        )
        if matching_value:
            error = (
                f"Invalid entry in username and/or password fields. Please try again."
            )
            return render_template("login.html", error=error)

        conn = sqlite3.connect("chal.db")
        cursor = conn.cursor()

        query = f"SELECT secret FROM login_details WHERE username = '{username}' AND password = '{password}';"

        result = cursor.execute(query)
        user = result.fetchone()

        conn.close()

        if user:
            session["logged_in"] = True
            session["username"] = username
            session["secret"] = user[0]
            return redirect(url_for("profile"))
        else:
            error = "Invalid login credentials. Please try again."
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/")
def index():
    if "logged_in" in session and session["logged_in"]:
        session.pop("logged_in", None)
        return redirect(url_for("index"))
    return render_template("landing.html")


@app.route("/profile")
def profile():
    if "logged_in" in session and session["logged_in"]:
        username = session["username"]
        secret = session.get("secret")
        key = "0"
        if "secret" not in str(secret):
            key = "1"
        return render_template(
            "profile.html", username=username, secret=secret, key=key
        )
    else:
        error = "You are not logged in. Please log in first."
        return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return render_template("login.html")


@app.after_request
def add_cache_control(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "-1"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
