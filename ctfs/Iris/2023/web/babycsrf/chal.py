from flask import Flask, request

app = Flask(__name__)

with open("home.html") as home:
    HOME_PAGE = home.read()

@app.route("/")
def home():
    return HOME_PAGE

@app.route("/api")
def page():
    secret = request.cookies.get("secret", "EXAMPLEFLAG")
    return f"setMessage('irisctf{{{secret}}}');"

app.run(port=12345)
