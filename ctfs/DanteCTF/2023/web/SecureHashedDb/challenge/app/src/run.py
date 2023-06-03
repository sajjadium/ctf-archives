from flask import Flask, render_template, request, session, redirect, jsonify, make_response
from flask_mysqldb import MySQL
from utils.db_connection import db_Connection as cnn
from utils.userUtils import userUtils as utl
from serverRequestHandler import serverHandler as server
from waitress import serve
import os


app = Flask(__name__)

# Inizialization Classes
utils = utl()
sqler = cnn(app, MySQL(), utils)

cursor = None
jwt_token = os.environ['JWT_SECRET']
backend = server()


@app.before_request
def updateConnection():
    global cursor
    cursor = sqler.initMySql()


@app.route('/')
def root():
    if not session or session['username'] != sqler.staticAdminSelector(cursor):
        return redirect('/getinfo/1')
    return redirect('/dashboard')


@app.route('/getinfo/<id>')
def dosomething(id):
    # I'm still learning sql + python
    # Method for code skills testing purposes
    try:
        user_id = int(id)
    except ValueError:
        return "Nope"
    cursor.execute(f"SELECT * FROM user WHERE id = ':{user_id}:'")
    rows = cursor.fetchall()
    resp = jsonify(rows)

    return resp


@app.route('/panel', methods=["GET", "POST"])
def panel():
    if session and session['username'] == sqler.staticAdminSelector(cursor):
        if request.method == "POST":
            key = request.form["key"]
            value = request.form["value"]
            backendResponseList = backend.sendRequest(key, value, jwt_token, utils)
            resp = make_response(render_template('dashboard.html', adminName=session['username'], display="yes", responseFromServer=backendResponseList[0]))
            resp.set_cookie("magicToken", backendResponseList[1])
            return resp

        return redirect('/dashboard')

    return redirect('/login')


@app.route('/getSignedCookie', methods=["POST"])
def getSignedCookie():
    if session and session['username'] == sqler.staticAdminSelector(cursor):
        if request.method == "POST":
            key = request.form["key"]
            value = request.form["value"]
            encoded_jwt = utils.jwtSignerMethod({key: value}, jwt_token)
            resp = make_response(render_template('dashboard.html', adminName=session['username'], display="none"))
            resp.set_cookie("magicToken", encoded_jwt)
            return resp

        return redirect('/dashboard')

    return redirect('/login')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if session and session['username'] == sqler.staticAdminSelector(cursor):
        return render_template("dashboard.html", adminName=session['username'], display="none", response_from_server="")
    return redirect('/login')


@app.route('/login', methods=["GET", "POST"])
def performLogin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "" or password == "":
            return render_template("login.html", displayStatus="block")

        login = sqler.queryExecutor(query=username, cursor=cursor)

        if (login):
            verified = utils.hash_verifier(password=password, recoveredPassword=login['password'])
            if verified:
                session['username'] = login['username']
                return redirect("/dashboard")

        return render_template("login.html", displayStatus="block")

    return render_template("login.html", displayStatus="none")


if __name__ == "__main__":
    app.secret_key = utils.generateRandomToken(16)
    serve(app, host='0.0.0.0', port=1999)
