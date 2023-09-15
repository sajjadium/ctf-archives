from flask import Flask, render_template, request, session, url_for, redirect,abort,jsonify, flash, send_file
import time
from collections import deque
from process import COMPANIES, processTransaction, loginDB, Throttle_Splash, threadTransact, market_scrape
from threading import Thread

app = Flask(__name__,static_folder="static")


def basic(req, *aargs):
    return isinstance(req, dict) and all((i in req.keys() for i in aargs))

@app.route("/buy", methods=['POST'])
def buy():
    if not basic(request.form, "key", "stock"):
        return abort(403)
    return processTransaction(request.form["key"], 1, request.form["stock"])

@app.route("/sell", methods=['POST'])
def sell():
    if not basic(request.form, "key", "stock"):
        return abort(403)
    return processTransaction(request.form["key"], 2, request.form["stock"])

@app.route("/trade", methods=['POST'])
def trade():
    if not basic(request.form, "key", "stock", "stock1"):
        return abort(403)
    return processTransaction(request.form["key"], 3, request.form["stock"],request.form["stock1"])

@app.route("/flag", methods=['POST'])
def flag():
    if not basic(request.form, "key"):
        return abort(403)
    return processTransaction(request.form["key"], 4, "flag")

@app.route("/listCalls")
def listCalls():
    return jsonify(COMPANIES)

@app.route("/login", methods=['POST'])
def login():
    if not basic(request.form):
        return abort(403)
    return jsonify(loginDB(request.form["key"]))

@app.route("/")
def index():
    return "Welcome to the City Subway Auctionstock Website (CSAW)!"

if __name__ == "__main__":
    thread1 = Thread(target=Throttle_Splash)
    thread2 = Thread(target=threadTransact)
    thread3 = Thread(target=market_scrape)

    thread1.start()
    thread2.start()
    thread3.start()

    app.run(host="0.0.0.0", port=4657, threaded=True)

