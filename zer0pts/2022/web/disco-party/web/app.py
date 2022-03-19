#!/usr/bin/env python3
import base64
import flask
import hashlib
import json
import os
import redis
import urllib.parse
import urllib.request

from secret import *

MESSAGE_LENGTH_LIMIT = 2000

# redis
DB_TICKET = 0
DB_BOT = 1

# recaptcha
RECAPTCHA_SITE_KEY = "6LfIGcYeAAAAAHRPxzy0PC5eyujDK45OW_B_q60w"
PROJECT_ID = "1075927595652"

def get_redis_conn(db):
    return redis.Redis(host='redis', port=6379, db=db)

def verify_recaptcha(token):
    if RECAPTCHA_SECRET is None:
        return 1

    body = json.dumps({
        "event": {
            "token": token,
            "siteKey": RECAPTCHA_SITE_KEY
        }
    }).encode()
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(
                f"https://recaptchaenterprise.googleapis.com/v1beta1/projects/{PROJECT_ID}/assessments?key={RECAPTCHA_SECRET}",
                headers={'Content-Type': 'application/json'},
                data=body
            )
        ).read()
    except:
        return -1

    result = json.loads(data)
    score = result.get("score", 0)
    assert isinstance(score, float) or isinstance(score, int)

    return score

# utils
def b64digest(b):
    return base64.urlsafe_b64encode(b).strip(b"=").decode()

def get_key(id):
    assert isinstance(id, str)
    return b64digest(hashlib.sha256((APP_KEY + id).encode()).digest())[:10]

# flask
app = flask.Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Home"""
    return flask.render_template(
        "index.html",
        is_post=False,
        title="Create Paste",
        sitekey=RECAPTCHA_SITE_KEY
    )

@app.route("/post/<string(length=16):id>", methods=["GET"])
def get_post(id):
    """Read a ticket"""
    # Get ticket by ID
    content = get_redis_conn(DB_TICKET).get(id)
    if content is None:
        return flask.abort(404, "not found")

    # Check if admin
    content = json.loads(content)
    key = flask.request.args.get("key")
    is_admin = isinstance(key, str) and get_key(id) == key

    return flask.render_template(
        "index.html",
        **content,
        is_post=True,
        panel=f"""
<strong>Hello admin! Your flag is: {FLAG}</strong><br>
<form id="delete-form" method="post" action="/api/delete">
    <input name="id" type="hidden" value="{id}">
    <input name="key" type="hidden" value="{key}">
    <button id="modal-button-delete" type="button">Delete This Post</button>
</form>
""" if is_admin else "",
        url=flask.request.url,
        sitekey=RECAPTCHA_SITE_KEY
    )

@app.route("/api/new", methods=["POST"])
def api_new():
    """Create a new ticket"""
    # Get parameters
    try:
        title = flask.request.form["title"]
        content = flask.request.form["content"]
    except:
        return flask.abort(400, "Invalid request")

    # Register a new ticket
    id = b64digest(os.urandom(16))[:16]
    get_redis_conn(DB_TICKET).set(
        id, json.dumps({"title": title, "content": content})
    )

    return flask.jsonify({"result": "OK",
                          "message": "Post created! Click here to see your post",
                          "action": f"{flask.request.url_root}post/{id}"})

@app.route("/api/delete", methods=["POST"])
def api_delete():
    """Delete a ticket"""
    # Get parameters
    try:
        id = flask.request.form["id"]
        key = flask.request.form["key"]
    except:
        return flask.abort(400, "Invalid request")

    if get_key(id) != key:
        return flask.abort(401, "Unauthorized")

    # Delete
    if get_redis_conn(DB_TICKET).delete(id) == 0:
        return flask.jsonify({"result": "NG", "message": "Post not found"})

    return flask.jsonify({"result": "OK", "message": "This post was successfully deleted"})

@app.route("/api/report", methods=["POST"])
def api_report():
    """Reoprt an invitation ticket"""
    # Get parameters
    try:
        url = flask.request.form["url"]
        reason = flask.request.form["reason"]
        recaptcha_token = flask.request.form["g-recaptcha-response"]
    except Exception:
        return flask.abort(400, "Invalid request")

    # Check reCAPTCHA
    score = verify_recaptcha(recaptcha_token)
    if score == -1:
        return flask.jsonify({"result": "NG", "message": "Recaptcha verify failed"})
    if score <= 0.3:
        return flask.jsonify({"result": "NG", "message": f"Bye robot (score: {score})"})

    # Check URL
    parsed = urllib.parse.urlparse(url.split('?', 1)[0])
    if len(parsed.query) != 0:
        return flask.jsonify({"result": "NG", "message": "Query string is not allowed"})
    if f'{parsed.scheme}://{parsed.netloc}/' != flask.request.url_root:
        return flask.jsonify({"result": "NG", "message": "Invalid host"})

    # Parse path
    adapter = app.url_map.bind(flask.request.host)
    endpoint, args = adapter.match(parsed.path)
    if endpoint != "get_post" or "id" not in args:
        return flask.jsonify({"result": "NG", "message": "Invalid endpoint"})

    # Check ID
    if not get_redis_conn(DB_TICKET).exists(args["id"]):
        return flask.jsonify({"result": "NG", "message": "Invalid ID"})

    key = get_key(args["id"])
    message = f"URL: {url}?key={key}\nReason: {reason}"

    try:
        get_redis_conn(DB_BOT).rpush(
            'report', message[:MESSAGE_LENGTH_LIMIT]
        )
    except Exception:
        return flask.jsonify({"result": "NG", "message": "Post failed"})

    return flask.jsonify({"result": "OK", "message": "Successfully reported"})

if __name__ == "__main__":
    app.run()
