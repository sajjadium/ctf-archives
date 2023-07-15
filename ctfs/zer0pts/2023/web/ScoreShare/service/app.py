#!/usr/bin/env python3
import flask
import os
import re
import redis

DEFAULT_CONFIG = {
    'template': {
        'title': 'Nyan Cat',
        'abc': open('nyancat.abc').read(),
        'link': 'https://en.wikipedia.org/wiki/Nyan_Cat'
    },
    'synth_options': [
        {'name': 'el', 'value': '#audio'},
        {'name': 'options', 'value': {
            'displayPlay': True,
            'displayRestart': True
        }}
    ]
}
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))

app = flask.Flask(__name__)
app.secret_key = os.urandom(16)

def db():
    if getattr(flask.g, '_redis', None) is None:
        flask.g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return flask.g._redis

@app.after_request
def after_request(response):
    csp  = ""
    csp += "default-src 'self';"
    csp += "script-src 'self';"
    csp += "style-src 'self' 'unsafe-inline';"
    csp += "object-src 'none';"
    csp += "frame-src *;"
    csp += "connect-src 'self' https://paulrosen.github.io"
    response.headers['Content-Security-Policy'] = csp
    return response

@app.route("/", methods=['GET', 'POST'])
def upload():
    if flask.request.method == 'POST':
        title = flask.request.form.get('title', '')
        abc = flask.request.form.get('abc', None)
        link = flask.request.form.get('link', '')
        if not title:
            flask.flash('Title is empty')
        elif not abc:
            flask.flash('ABC notation is empty')
        else:
            sid = os.urandom(16).hex()
            db().hset(sid, 'title', title)
            db().hset(sid, 'abc', abc)
            db().hset(sid, 'link', link)
            return flask.redirect(flask.url_for('score', sid=sid))
    return flask.render_template("upload.html")

@app.route("/score/<sid>")
def score(sid: str):
    """Score viewer"""
    title = db().hget(sid, 'title')
    link = db().hget(sid, 'link')
    if link is None:
        flask.flash("Score not found")
        return flask.redirect(flask.url_for('upload'))
    return flask.render_template("score.html", sid=sid, link=link.decode(), title=title.decode())

@app.route("/api/config")
def api_config():
    return DEFAULT_CONFIG

@app.route("/api/score/<sid>")
def api_score(sid: str):
    abc = db().hget(sid, 'abc')
    if abc is None:
        return flask.abort(404)
    else:
        return flask.Response(abc)

if __name__ == '__main__':
    app.run()
