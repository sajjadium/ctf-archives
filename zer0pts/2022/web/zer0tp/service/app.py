import base64
import flask
import hashlib
import os
import redis
import zlib

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)

"""
[ How does Zer0TP work? ]
+--------+        +-------------+
| Zer0TP |<------>| third party |
+--------+    e   +-------------+
  ^  ^  |            ^
 a| b| c|            |
  |  |  v           d|
+--------+           |
|  user  |-----------+
+--------+

Third party software can use zer0tp as its authentication scheme.
a. The user registers an account on zer0tp
b. User logs in to zer0tp to issue an OTP
c. zer0tp will issue a client token
d. User sends the client token to the third part software
e. Third part software can authenticate the user by the token

[ Why Zer0TP? ]
Your service no longer needs to prepare database for login feature!
Also the users don't have to send their passwords to your website.
It's good both for you and for the users :)
"""

@app.route("/")
def home():
    return flask.render_template("index.html")

@app.route("/update")
def update():
    return flask.render_template("update.html")

@app.route("/api/register", methods=["POST"])
def register():
    username = flask.request.form.get("username", "").encode()
    password = flask.request.form.get("password", "").encode()
    if not 4 <= len(username) < 50:
        return flask.jsonify({"result": "error",
                              "reason": "Username is too short or long"})
    if not 8 <= len(password) < 128:
        return flask.jsonify({"result": "error",
                              "reason": "Password is too short or long"})

    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    if r.exists(username):
        return flask.jsonify({"result": "error",
                              "reason": "This user already exists"})

    r.hmset(username,
            {"pass": hashlib.sha256(password).hexdigest(), "admin": 0})
    return flask.jsonify({"result": "OK"})

@app.route("/api/login", methods=["POST"])
def login():
    username = flask.request.form.get("username", "").encode()
    password = flask.request.form.get("password", "").encode()

    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    passhash = r.hget(username, 'pass')
    if passhash is None or \
       passhash.decode() != hashlib.sha256(password).hexdigest():
        return flask.jsonify({"result": "error",
                              "reason": "The username or password is wrong"})

    id = os.urandom(8).hex()
    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    secret = r.get(username)
    if secret is None:
        secret = base64.b64encode(os.urandom(12))
        r.set(username, secret)
        r.expire(username, 60*30)

    token = zlib.compress(username + secret)[:8]
    return flask.jsonify({"result": "OK",
                          "id": id,
                          "token": hashlib.md5(id.encode() + token).hexdigest()})

@app.route("/api/rename", methods=["POST"])
def rename():
    username = flask.request.form.get("username", "").encode()
    password = flask.request.form.get("password", "").encode()
    new_username = flask.request.form.get("new_username", "").encode()
    new_password = flask.request.form.get("new_password", "").encode()

    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    passhash = r.hget(username, 'pass')
    if passhash is None or \
       passhash.decode() != hashlib.sha256(password).hexdigest():
        return flask.jsonify({"result": "error",
                              "reason": "The username or password is wrong"})

    if not 4 <= len(new_username) < 50:
        return flask.jsonify({"result": "error",
                              "reason": "Username is too short or long"})
    if not 8 <= len(new_password) < 128:
        return flask.jsonify({"result": "error",
                              "reason": "Password is too short or long"})
    if r.exists(new_username):
        return flask.jsonify({"result": "error",
                              "reason": "This user already exists"})

    r.rename(username, new_username)
    r.hset(new_username, 'pass', hashlib.sha256(new_password).hexdigest())

    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    if r.exists(username):
        r.rename(username, new_username)

    return flask.jsonify({"result": "OK"})

@app.route("/api/auth", methods=["GET"])
def authenticate():
    username = flask.request.args.get("username", "").encode()
    req_id = flask.request.args.get("id", "").encode()
    req_token = flask.request.args.get("token", "")

    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    secret = r.get(username)
    if secret is None:
        return flask.jsonify({"result": "error", "reason": "User not found or token expired"})

    token = zlib.compress(username + secret)[:8]
    if req_token == hashlib.md5(req_id + token).hexdigest():
        return flask.jsonify({"result": "OK"})
    else:
        return flask.jsonify({"result": "error", "reason": "Invalid token"})

@app.route("/api/is_admin", methods=["GET"])
def is_admin():
    username = flask.request.args.get("username", "").encode()

    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    admin = r.hget(username, 'admin')
    if admin is None:
        return flask.jsonify({"result": "error",
                              "reason": "Account not found"})

    return flask.jsonify({"result": "OK", "is_admin": int(admin)})

@app.route("/api/set_admin", methods=["POST"])
def set_admin():
    # Apply for enterprise plan to use this feature :)
    username = flask.request.form.get("username", "").encode()
    req_secret = flask.request.form.get("secret", "").encode()
    admin = flask.request.form.get("admin", "0")

    r = redis.Redis(host=REDIS_HOST, port=6379, db=1)
    secret = r.get(username)
    if secret is None:
        return flask.jsonify({"result": "error",
                              "reason": "User not found or token expired"})

    if secret != req_secret:
        return flask.jsonify({"result": "error",
                              "reason": "Access denied"})

    r = redis.Redis(host=REDIS_HOST, port=6379, db=0)
    data = r.hgetall(username)
    if data is None:
        return flask.jsonify({"result": "error",
                              "reason": "Account not found"})

    if admin == '1':
        r.hset(username, "admin", 1)
    else:
        r.hset(username, "admin", 0)

    return flask.jsonify({"result": "OK"})

if __name__ == '__main__':
    app.run(port=8080)
