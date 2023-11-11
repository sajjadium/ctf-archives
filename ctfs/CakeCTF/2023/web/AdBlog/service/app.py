import base64
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

    blog_id = os.urandom(32).hex()
    title = flask.request.form.get('title', 'untitled')
    content = flask.request.form.get('content', '<i>empty post</i>')
    if len(title) > 128 or len(content) > 1024*1024:
        return flask.render_template("index.html",
                                     msg="Too long title or content.")

    db().set(blog_id, json.dumps({'title': title, 'content': content}))
    return flask.redirect(f"/blog/{blog_id}")

@app.route('/blog/<blog_id>')
def blog(blog_id):
    if not re.match("^[0-9a-f]{64}$", blog_id):
        return flask.redirect("/")

    blog = db().get(blog_id)
    if blog is None:
        return flask.redirect("/")

    blog = json.loads(blog)
    title = blog['title']
    content = base64.b64encode(blog['content'].encode()).decode()
    return flask.render_template("blog.html", title=title, content=content)


def db():
    if getattr(flask.g, '_redis', None) is None:
        flask.g._redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    return flask.g._redis

if __name__ == '__main__':
    app.run()
