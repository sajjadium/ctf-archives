from flask import Flask, request, g, send_file, redirect, make_response
import secrets
from urllib.parse import urlparse
import re
from functools import wraps
import copy

host = re.compile("^[a-z0-9\.:]+$")

app = Flask(__name__)

NOTES = {}

def check_request(f):
    @wraps(f)
    def inner(*a, **kw):
        secFetchDest = request.headers.get('Sec-Fetch-Dest', None)
        if secFetchDest and secFetchDest != 'iframe': return "Invalid request"
        return f(*a, **kw)
    return inner

@app.after_request
def csp(response):
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-src 'self';";
    if "image_url" in g:
        url = g.image_url
        parsed = urlparse(url)
        if host.match(parsed.netloc) and parsed.scheme in ["http", "https"]:
            response.headers["Content-Security-Policy"] += "img-src " + parsed.scheme + "://" + parsed.hostname + ";"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    return response

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/home")
@check_request
def home():
    return """<!DOCTYPE html>
<body>
<form action='/create' method='post'><input type="text" id="title" name="title" placeholder="title"><br>
<input type="textarea" id="text" name="text" placeholder="note text"><br>
<input type="text" id="image" name="image" placeholder="image URL"><br>
<button type="submit">Create</button></form>
<a href='/search'>All Notes</a>
<form action='/search' method='get'><input type="text" id="query" name="query" placeholder="text"> <button type="submit">Search</button></form>
</body>"""

@app.route("/create", methods=["POST"])
@check_request
def create():
    if "<" in request.form.get("text", "(empty)") or \
            "<" in request.form.get("title", "(empty)") or \
            "<" in request.form.get("image", ""):
        return "Really?"

    user = request.cookies.get("user", None)
    if user is None:
        user = secrets.token_hex(16)

    note = {"id": secrets.token_hex(16), "text": request.form.get("text", "(empty)"), "image": request.form.get("image", None), "title": request.form.get("title", "(empty)"), "owner": user}
    NOTES[note["id"]] = note

    r = redirect("/note/" + note["id"])
    r.set_cookie('user', user, secure=True, httponly=True, samesite='None')
    return r

def render_note(note):
    data = "<!DOCTYPE html><body><b>" + note["title"] + "</b><br/>" + note["text"]
    if note["image"] is not None:
        g.image_url = note["image"]
        data += "<br/><img width='100%' src='" + note["image"] + "' crossorigin />"
    data += "</body>"
    return data

@app.route("/note/<nid>")
@check_request
def note(nid):
    if nid not in NOTES:
        return "?"
    return render_note(NOTES[nid])

@app.route("/search")
@check_request
def search():
    query = request.args.get("query", "")
    user = request.cookies.get("user", None)
    results = []
    notes_copy = copy.deepcopy(NOTES)
    for note in notes_copy.values():
        if note["owner"] == user and (query in note["title"] or query in note["text"]):
            results.append(note)
            if len(results) >= 5:
                break

    if len(results) == 0:
        return "<!DOCTYPE html><body>No notes.</body>"

    if len(results) == 1:
        return render_note(results[0])
    
    return "<!DOCTYPE html><body>" + "".join("<a href='/note/" + note["id"] + "'>" + note["title"] + "</a> " for note in results) + "</body>"
