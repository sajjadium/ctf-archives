import flask
import json
import os
import re
import redis
import requests

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_HOST", "6379"))
RECAPTCHA_KEY = os.getenv("RECAPTCHA_KEY", None)

app = flask.Flask(__name__)

def db():
    if getattr(flask.g, '_redis', None) is None:
        flask.g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=1)
    return flask.g._redis

def recaptcha(response):
    if RECAPTCHA_KEY is None:
        # Players' environment
        return True
    r = requests.post("https://www.google.com/recaptcha/api/siteverify",
                      params={'secret': RECAPTCHA_KEY,
                              'response': response})
    return json.loads(r.text)['success']

@app.route("/", methods=['GET', 'POST'])
def report():
    error = ok = ""
    if flask.request.method == 'POST':
        blog_id = str(flask.request.form.get('url', ''))
        response = flask.request.form.get('g-recaptcha-response')
        if not re.match("^[0-9a-f]{64}$", blog_id):
            error = 'Invalid blog ID'
        elif not recaptcha(response):
            error = "reCAPTCHA failed."
        else:
            db().rpush('report', f"blog/{blog_id}")
            ok = "Admin will check it soon."
    return flask.render_template("index.html", ok=ok, error=error)

if __name__ == '__main__':
    app.run(debug=True)
