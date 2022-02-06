#!/usr/bin/env python3

from flask import Flask
from flask import render_template
from flask import request

from flask_caching import Cache

app = Flask(__name__)

cache = Cache(config={'CACHE_TYPE': 'FileSystemCache', 'CACHE_DIR':'/tmp/vault', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

@app.after_request
def add_headers(response):
    response.headers['Content-Security-Policy'] = "frame-ancestors 'none';"
    response.headers['Cache-Control'] = 'no-store'
    return response

@app.route("/<path:vault_key>", methods=["GET", "POST"])
def vault(vault_key):
    parts = list(filter(lambda s: s.isdigit(), vault_key.split("/")))
    level = len(parts)
    if level > 15:
        return "Too deep", 404

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
    return render_template("vault.html", values = values, level = level), 404

@app.get("/")
def main():
    return render_template("main.html"), 404
