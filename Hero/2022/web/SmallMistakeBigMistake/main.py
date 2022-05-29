#!/usr/bin/env python
from flask import Flask, session, render_template

from string import hexdigits
from random import choice
from os import getenv


app = Flask(__name__)
app.secret_key = choice(hexdigits) * 32


@app.route("/", methods=["GET"])
def index():
    flag = "You are not admin !"
    if session and session["username"] == "admin":
        flag = getenv("FLAG")

    return render_template("index.html", flag=flag)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(getenv("PORT")))
