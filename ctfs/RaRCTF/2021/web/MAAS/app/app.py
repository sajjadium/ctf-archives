from flask import Flask, render_template, request, session, redirect, jsonify
import requests
import jsonschema

import os
import json
import sys

app = Flask(__name__)

ERR_MISSING = "Missing required parameters"


@app.route('/')
def index():
    html = """<html><head><title>MAAS</title></head>
<body><a href=/calculator>Calculator</a><br>
<a href=/notes>Notes</a><br>
<a href=/manager>Manager</a>"""
    return html

@app.route('/calculator', methods=["POST", "GET"])
def calculator():
    if request.method == "GET":
        return render_template('calculator.html')
    mode = request.form.get('mode')
    if not mode:
        return ERR_MISSING, 422
    if mode == 'checkers':
        value = request.form.get('value')
        if not value:
            return ERR_MISSING, 422
        body = {"value": value}
        if request.form.get('even'):
            body['even'] = True
        elif request.form.get('odd'):
            body['odd'] = True
        elif request.form.get('number'):
            body['number'] = True
        else:
            return ERR_MISSING, 422
        r = requests.post('http://calculator:5000/checkers', data=body)
        return render_template('calculator.html', tab='checkers', result=r.text)
    elif mode == 'arithmetic':
        n1 = request.form.get('n1')
        n2 = request.form.get('n2')
        if not n1 or not n2:
            return ERR_MISSING, 422
        body = {"n1": n1, "n2": n2}
        if request.form.get('add'):
            body['add'] = True
        elif request.form.get('sub'):
            body['sub'] = True
        elif request.form.get('div'):
            body['div'] = True
        elif request.form.get('mul'):
            body['mul'] = True
        else:
            return ERR_MISSING, 422
        r = requests.post('http://calculator:5000/arithmetic', data=body)
        return render_template('calculator.html', tab='arithmetic', result=r.text)


@app.route('/notes')
def notes_page():
    html = """
<head>
   <title>Notes</title>
   <link rel="stylesheet" href="static/css/style.css"/>
   <script src="static/js/app.js"></script>
</head>
<body>
<ul>
   <li><a href="/calculator">Calculator</a></li>
   <li><a href="/notes">Notes</a></li>
   <li><a href="/manager">Manager</a></li>
</ul><hr><br>
<a href=/notes/register>Register</a>"""
    return html


@app.route('/notes/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    data = {"mode": "register", "username": request.form.get("username")}
    requests.post("http://notes:5000/useraction", data=data)
    session["notes-username"] = request.form.get("username")
    return redirect("/notes/profile")


def render_bio(username, userdata):
    data = {"username": username,
            "mode": "bioget"}
    r = requests.post("http://notes:5000/useraction", data=data)
    try:
        r = requests.post("http://notes:5000/render", json={"bio": r.text, "data": userdata})
        return r.text
    except:
        return "Error in bio"


def userdata(username):
    data = {"username": session.get("notes-username"),
            "mode": "getdata"}
    r = requests.post("http://notes:5000/useraction", data=data)
    data = json.loads(r.text)
    if len(data) > 0:
        return json.loads(r.text)[0]
    else:
        return {}


@app.route('/notes/profile', methods=["POST", "GET"])
def profile():
    username = session.get('notes-username')
    if not username:
        return redirect('/notes/register')
    uid = requests.get(f"http://notes:5000/getid/{username}").text
    if request.method == "GET":
        return render_template("profile.html",
                               bio=render_bio(username, userdata(username)),
                               userid=uid
                               )
    mode = request.form.get("mode")
    if mode == "adddata":
        data = {"key": request.form.get("key"), "value": request.form.get("value"),
                "username": username,
                "mode": "adddata"}
        requests.post("http://notes:5000/useraction", data=data)
    elif mode == "bioadd":
        data = {"bio": request.form.get("bio"),
                "username": username,
                "mode": "bioadd"}
        requests.post("http://notes:5000/useraction", data=data)
    elif mode == "keytransfer":
        data = {"username": username,
                "host": request.form.get("host"),
                "port": request.form.get("port"),
                "key": request.form.get("key"),
                "mode": "keytransfer"}
        requests.post("http://notes:5000/useraction", data=data)
    return render_template("profile.html",
                           bio=render_bio(username, userdata(username)),
                           userid=uid
                           )


@app.route("/manager/login", methods=["POST"])
def manager_login():
    username = request.form.get("username")
    password = request.form.get("password")
    r = requests.post("http://manager:5000/login", json={
        "username": username,
        "password": password
    })
    response = r.json()
    if response.get('error'):
        return response['error'], 403
    session['managerid'] = response['uid']
    session['managername'] = response['name']
    if response.get('flag'):
        session['flag'] = response['flag']
    return redirect("/manager")


@app.route("/manager/update", methods=["POST"])
def manager_update():
    schema = {"type": "object",
              "properties": {
                  "id": {
                      "type": "number",
                      "minimum": int(session['managerid'])
                  },
                  "password": {
                      "type": "string",
                      "minLength": 10
                  }
              }}
    try:
        jsonschema.validate(request.json, schema)
    except jsonschema.exceptions.ValidationError:
        return jsonify({"error": f"Invalid data provided"})
    return jsonify(requests.post("http://manager:5000/update",
                                 data=request.get_data()).json())


@app.route("/manager")
def manager_index():
    return render_template("manager.html",
                           username=session.get("managername"),
                           flag=session.get("flag")
                           )


if __name__ == '__main__':
    app.config["SECRET_KEY"] = os.urandom(24)
    app.run(host='0.0.0.0', port=5000)
