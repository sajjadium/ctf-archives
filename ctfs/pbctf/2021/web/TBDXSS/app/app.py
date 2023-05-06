from flask import Flask, request, session, jsonify, Response
import json
import redis
import random
import os
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tops3cr3t")

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

HOST = os.environ.get("CHALL_HOST", "localhost:5000")

r = redis.Redis(host='redis')

@app.after_request
def add_XFrame(response):
    response.headers['X-Frame-Options'] = "DENY"
    return response


@app.route('/change_note', methods=['POST'])
def add():
    session['note'] = request.form['data']
    session.modified = True
    return "Changed succesfully"

@app.route("/do_report", methods=['POST'])
def do_report():
    cur_time = time.time()
    ip = request.headers.get('X-Forwarded-For').split(",")[-2].strip() #amazing google load balancer

    last_time = r.get('time.'+ip) 
    last_time = float(last_time) if last_time is not None else 0
    
    time_diff = cur_time - last_time

    if time_diff > 6:
        r.rpush('submissions', request.form['url'])
        r.setex('time.'+ip, 60, cur_time)
        return "submitted"

    return "rate limited"

@app.route('/note')
def notes():
    print(session)
    return """
<body>
{}
</body>
    """.format(session['note'])

@app.route("/report", methods=['GET'])
def report():
    return """
<head>
    <title>Notes app</title>
</head>
<body>
    <h3><a href="/note">Get Note</a>&nbsp;&nbsp;&nbsp;<a href="/">Change Note</a>&nbsp;&nbsp;&nbsp;<a href="/report">Report Link</a></h3>
        <hr>
        <h3>Please report suspicious URLs to admin</h3>
        <form action="/do_report" id="reportform" method=POST>
        URL: <input type="text" name="url" placeholder="URL">
        <br>
        <input type="submit" value="submit">
        </form>
    <br>
</body>
    """

@app.route('/')
def index():
    return """
<head>
    <title>Notes app</title>
</head>
<body>
    <h3><a href="/note">Get Note</a>&nbsp;&nbsp;&nbsp;<a href="/">Change Note</a>&nbsp;&nbsp;&nbsp;<a href="/report">Report Link</a></h3>
        <hr>
        <h3> Add a note </h3>
        <form action="/change_note" id="noteform" method=POST>
        <textarea rows="10" cols="100" name="data" form="noteform" placeholder="Note's content"></textarea>
        <br>
        <input type="submit" value="submit">
        </form>
    <br>
</body>
    """

