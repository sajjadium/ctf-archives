import flask
import json
import os
import requests

HOST = os.getenv("HOST", "localhost")
ZER0TP_HOST = os.getenv("ZER0TP_HOST", "localhost")
ZER0TP_PORT = os.getenv("ZER0TP_PORT", "8080")
FLAG = os.getenv("FLAG", "nek0pts{*** REDUCTED ***}")

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/login", methods=["GET", "POST"])
def login():
    if flask.request.method == 'GET':
        return flask.render_template("login.html",
                                     HOST=HOST, PORT=ZER0TP_PORT)

    username = flask.request.form.get("username", "")
    id = flask.request.form.get("id", "").encode()
    token = flask.request.form.get("token", "").encode()

    # We don't need to prepare DB thanks to Zer0TP :)
    r = requests.get(f"http://{ZER0TP_HOST}:{ZER0TP_PORT}/api/auth",
                     params={"username": username, "id": id, "token": token})
    resp = json.loads(r.text)
    if resp['result'] == 'OK':
        flask.session['username'] = username
    else:
        flask.flash(f"Authentication failed ({resp['reason']})")

    return flask.redirect("/")

@app.route("/logout", methods=["GET"])
def logout():
    if 'username' in flask.session:
        del flask.session['username']

    return flask.redirect("/")

@app.route("/")
def home():
    if 'username' not in flask.session:
        return flask.redirect("/login")

    # You can also manage admin users if you're using
    # the enterprise plan (1337 USD/month)
    r = requests.get(f"http://{ZER0TP_HOST}:{ZER0TP_PORT}/api/is_admin",
                     params={"username": flask.session['username']})
    is_admin = json.loads(r.text)["is_admin"]

    return flask.render_template("index.html",
                                 flag=FLAG,
                                 is_admin=is_admin,
                                 username=flask.session['username'])

if __name__ == '__main__':
    app.run(port=8077)
