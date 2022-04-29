#!/usr/bin/env python

from flask import Flask, Response, abort, request, render_template
import random
from string import *
import re

app = Flask(__name__)

flag = open("flag.txt").read()
users = open("users.txt").read()

users += flag


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("lookup.html")
    if request.method == "POST":
        name = request.form["name"]
        setting = int(request.form["setting"])
        if name:
            if name[0].isupper():
                name = name[1:]

        results = re.findall(r"[A-Z][a-z]*?" + name + r"[a-z]*?\n", users, setting)
        results = [x.strip() for x in results if x or len(x) > 1]

        return render_template("lookup.html", passed_results=True, results=results)


if __name__ == "__main__":
    app.run()
