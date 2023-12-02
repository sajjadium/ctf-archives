#!/usr/local/bin/python

from flask import Flask, render_template, request, Response
import requests

app = Flask(__name__,
            static_url_path='',
            static_folder="static")

@app.route("/fetchdata", methods=["POST"])
def fetchdata():
    url = request.form["url"]

    if "127" in url:
        return Response("No loopback for you!", mimetype="text/plain")
    if url.count('.') > 2:
        return Response("Only 2 dots allowed!", mimetype="text/plain")
    if "x" in url:
        return Response("I don't like twitter >:(" , mimetype="text/plain") 
    if "flag" in url:
        return Response("It's not gonna be that easy :)", mimetype="text/plain")

    try:
        res = requests.get(url)
    except Exception as e:
        return Response(str(e), mimetype="text/plain")

    return Response(res.text[:32], mimetype="text/plain")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
