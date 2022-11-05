from flask import Flask, request
import os
from dotenv import load_dotenv

load_dotenv()

flag = os.getenv("FLAG")

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "<p>Whoa! You must be someone important </p>"

@app.route("/flag", methods=["GET"])
def get_flag():
    print(request.remote_addr, " Sent flag")
    return f"Here's your flag: {flag}"