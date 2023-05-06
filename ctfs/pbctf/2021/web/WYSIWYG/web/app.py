#!/usr/bin/env python3

import os
import socket

from flask import Flask
from flask import render_template
from flask import request

from flask_recaptcha import ReCaptcha

app = Flask(__name__)
app.config["RECAPTCHA_SITE_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_SECRET_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]
recaptcha = ReCaptcha(app)


@app.route("/tinymce/")
def tinymce():
    return render_template("tinymce.html")


@app.route("/froala/")
def froala():
    return render_template("froala.html")


@app.route("/ckeditor/")
def ckeditor():
    return render_template("ckeditor.html")


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main.html")
    else:
        if recaptcha.verify():
            text = request.form.get("text")
            if not text:
                return "The text parameter is required", 422

            s = socket.create_connection(("bot", 8000))
            s.sendall(text.encode())
            resp = s.recv(100)
            s.close()

            return resp.decode(), 200
        else:
            return "Invalid captcha", 422
