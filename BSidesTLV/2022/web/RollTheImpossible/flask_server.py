import os
import challenge
from flask import Flask, session, render_template

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(32))

@app.route("/")
def init():
    challenge.init()
    return render_template("index.html")

@app.route("/step", methods=["POST"])
def step():
    return challenge.step()
