#!/usr/bin/python3

from flask import Flask, request, render_template, url_for, make_response
from flask_caching import Cache, CachedResponse
from urllib.parse import urlencode
import requests
from config import URL

app = Flask(__name__)
app.config.from_object('config.BaseConfig') 
cache = Cache(app)


FLAG = "shellmates{bla_bla_bla}"

def make_cache_key():
    args = request.form
    key = request.path + '?' + urlencode([
        (k, v) for k in sorted(args) for v in sorted(args.getlist(k))
    ])
    key += urlencode([('User-Agent', request.headers['User-Agent'])])
    return key

@app.route("/", methods=["GET", "POST", "HEAD"])
@cache.cached(timeout=30, key_prefix=make_cache_key)
def check_note():

    if request.method == "GET":
        return render_template("./index.html")
    elif request.method == "POST":
        note_file = request.form.get("note")
        try:
            note_path = url_for("static",filename=f"notes/{note_file}")
            r = requests.get(f"{URL}{note_path}")
            if r.status_code == 200:
                result = "Note is available"
                return CachedResponse(
                    response=make_response(
                        render_template(
                            "./index.html", result=result
                        )
                    )
                    ,timeout=50,
                )
            else:
                result = "Note is not available"
                return CachedResponse(
                    response=make_response(
                        render_template(
                            "./index.html", result=result
                        )
                    )
                    ,timeout=50,
                )
        except Exception as e:
            print(e)
            result = "Note is not available"
            return CachedResponse(
                response=make_response(
                    render_template(
                        "./index.html", result=result
                    )
                )
                ,timeout=50,
            )
    else:
        return render_template("./index.html")


@app.route("/magic_note", methods=["GET", "HEAD"])
@cache.cached(timeout=5, key_prefix=make_cache_key)
def magic_note():
    if request.method == "GET":

        if request.remote_addr == "127.0.0.1":
            return CachedResponse(
                response=make_response(
                    render_template(
                        "./magic_note.html", result=FLAG
                    )
                )
                ,timeout=50,
            )
        else:
            return CachedResponse(
                response=make_response(
                    render_template(
                        "./magic_note.html"
                    )
                )
                ,timeout=50,
            )

    else:
        return render_template("./magic_note.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=False)