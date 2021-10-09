#!/usr/bin/env python3

import os
import socket


from flask import Flask
from flask import render_template
from flask import request

from flask_caching import Cache
from flask_recaptcha import ReCaptcha

app = Flask(__name__)
app.config["RECAPTCHA_SITE_KEY"] = os.environ["RECAPTCHA_SITE_KEY"]
app.config["RECAPTCHA_SECRET_KEY"] = os.environ["RECAPTCHA_SECRET_KEY"]
recaptcha = ReCaptcha(app)

cache = Cache(config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR':'/tmp/vault', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

@app.route("/<path:vault_key>", methods=["GET", "POST"])
def vault(vault_key):
    parts = list(filter(lambda s: s.isdigit(), vault_key.split("/")))
    level = len(parts)
    if level > 15:
        return "Too deep", 422

    if not cache.get("vault"):
        cache.set("vault", {})

    main_vault = cache.get("vault")

    c = main_vault
    for v in parts:
        c = c.setdefault(v, {})
    
    values = c.setdefault("values", [])

    if level > 8 and request.method == "POST":
         value = request.form.get("value")
         value = value[0:50]
         values.append(value)

    cache.set("vault", main_vault)
    return render_template("vault.html", values = values, level = level)

@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        return render_template("main.html")
    else:
        if recaptcha.verify():
            url = request.form.get("url")
            if not url:
                return "The url parameter is required", 422
            if not url.startswith("https://") and not url.startswith("http://"):
                return "The url parameter is invalid", 422


            s = socket.create_connection(("bot", 8000))
            s.sendall(url.encode())
            resp = s.recv(100)
            s.close()

            return resp.decode(), 200
        else:
            return "Invalid captcha", 422
