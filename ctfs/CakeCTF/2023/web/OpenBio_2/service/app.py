import bleach
import flask
import json
import os
import re
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = flask.Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template("index.html")

    err = None
    bio_id = os.urandom(32).hex()
    name = flask.request.form.get('name', 'Anonymous')
    email = flask.request.form.get('email', '')
    bio1 = flask.request.form.get('bio1', '')
    bio2 = flask.request.form.get('bio2', '')
    if len(name) > 20:
        err = "Name is too long"
    elif len(email) > 40:
        err = "Email is too long"
    elif len(bio1) > 1001 or len(bio2) > 1001:
        err = "Bio is too long"

    if err:
        return flask.render_template("index.html", err=err)

    db().set(bio_id, json.dumps({
        'name': name, 'email': email, 'bio1': bio1, 'bio2': bio2
    }))
    return flask.redirect(f"/bio/{bio_id}")

@app.route('/bio/<bio_id>')
def bio(bio_id):
    if not re.match("^[0-9a-f]{64}$", bio_id):
        return flask.redirect("/")

    bio = db().get(bio_id)
    if bio is None:
        return flask.redirect("/")

    bio = json.loads(bio)
    name = bio['name']
    email = bio['email']
    bio1 = bleach.linkify(bleach.clean(bio['bio1'], strip=True))[:10000]
    bio2 = bleach.linkify(bleach.clean(bio['bio2'], strip=True))[:10000]
    return flask.render_template("bio.html",
                                 name=name, email=email, bio1=bio1, bio2=bio2)


def db():
    if getattr(flask.g, '_redis', None) is None:
        flask.g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return flask.g._redis

if __name__ == '__main__':
    app.run()
