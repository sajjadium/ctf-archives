import subprocess
import os, stat
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/challenge")
def palindrome_challenge():
    user_code = request.json["code"]
    cmd = ["timeout", "-s", "KILL", os.environ.get('TIMEOUT', '10'), "sudo", "-u", "safe_eval", "python", "palindrome_challenge.py", user_code]
    try:
        res = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        res = "Exception"
    if res not in ["Solved", "Not solved", "SyntaxError", "Exception"]:
        res = "Not solved"
    return {"result": res}
