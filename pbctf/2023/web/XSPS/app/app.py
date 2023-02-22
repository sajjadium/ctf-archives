from flask import Flask, request, session, jsonify, Response, make_response, g
import json
import redis
import random
import os
import binascii
import time

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "tops3cr3t")

app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    # SESSION_COOKIE_SAMESITE='Lax',
)

HOST = os.environ.get("CHALL_HOST", "localhost:5000")

r = redis.Redis(host='redis')

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

@app.before_request
def rand_nonce():
    g.nonce = binascii.b2a_hex(os.urandom(15)).decode()

@app.after_request
def add_CSP(response):
    response.headers['Content-Security-Policy'] = f"default-src 'self'; script-src 'nonce-{g.nonce}'"
    return response


@app.route('/add_note', methods=['POST'])
def add():
    if 'notes' not in session:
        session['notes'] = {}
    session['notes'][request.form['name']] = request.form['data']
    if 'highlight_note' in request.form and request.form['highlight_note'] == "YES":
        session['highlighted_note'] = request.form['name']

    session.modified = True
    return "Changed succesfully"


@app.route('/notes')
def notes():
    if 'notes' not in session:
        return []
    return [X for X in session['notes']] 

@app.route("/highlighted_note")
def highlighted_note():
    if 'highlighted_note' not in session:
        return {'name':False}
    return session['highlighted_note']

@app.route('/note/<path:name>')
def get_note(name):
    if 'notes' not in session:
        return ""
    if name not in session['notes']:
        return ""
    return session['notes'][name]

@app.route('/static/<path:filename>')
def static_file(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return f"""
<head>
    <title>Notes app</title>
</head>
<body>
    <script nonce='{g.nonce}' src="/static/js/main.js"></script>

    <h3><a href="/report">Report Link</a></h3>
        <hr>
        <h3> Highlighted Note </h3>
        <div id="highlighted"></div>
        <hr>
        <h3> Add a note </h3>
        <form action="/add_note" id="noteform" method=POST>
        <input type=text name="name" placeholder="Note's name">
        <br>
        <br>
        <textarea rows="10" cols="100" name="data" form="noteform" placeholder="Note's content"></textarea>
        <br>
        <br>
        <input type="checkbox" name="highlight_note" value="YES">
        <label for="vehicle1">Highlight Note</label><br>
        <br>
        <input type="submit" value="submit">
        </form>
    <hr>
    <h3>Search Note</h3>
    <a id=search_result></a>
    <input id='search_content' type=text name="name" placeholder="Content to search">
        <input id='search_open' type="checkbox" name="open_after" value="YES">
        <label for="open">Open</label><br>
    <br>
    <input id='search_button' type="submit" value="submit">

</body>
    """

