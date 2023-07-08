from flask import Flask, render_template, request
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)

FLAG = open("./flag.txt", "r").read()

@app.route("/", methods = ["GET"])
def index():
    return render_template("index.tpl")

@app.route("/flag", methods = ["GET"])
def flag():
    remote_ip = request.headers.get("X-Real-IP", "0.0.0.0")
    if not remote_ip.startswith("10.25.25."):
        raise Unauthorized("Internal clients only.")
    return render_template("flag.tpl", flag=FLAG)

if __name__ == "__main__":
    app.run("127.0.0.1", 8080)