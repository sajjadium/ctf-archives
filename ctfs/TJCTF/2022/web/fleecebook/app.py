from flask import Flask, request, render_template, render_template_string, redirect, send_from_directory
from db import conn_db
from uuid import uuid4

conn, cur = conn_db()

app = Flask(__name__, static_url_path='')


@app.route('/static/<path:path>')
def static_file(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    posts = cur.execute('SELECT * FROM posts LIMIT 5;').fetchall()

    return render_template('index.html', posts=posts)


@app.route('/post', methods=['GET', 'POST'])
def make_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if title is None or content is None:
            return 'missing title and/or content', 400

        id = str(uuid4())

        cur.execute(
            'INSERT INTO posts (id, title, content) VALUES (?, ?, ?);', (id, title, content))

        conn.commit()

        return redirect('/post/' + id)
    else:
        return render_template('make_post.html')


@app.route('/post/<id>')
def view_post(id):
    # view post
    post = cur.execute('SELECT * FROM posts WHERE id = ?;', (id, )).fetchone()

    if post is None:
        return 'fleece could not be found </3', 404

    post_format = """
    {{ title }} - {{ timestamp }}
    <br>
    {{ content }}
    """

    return render_template_string(post_format, title=post[1], content=post[2], timestamp=post[3])


@app.errorhandler(404)
def not_found(e):
    return 'your fleece page (' + request.path + ') could not be found :notlikefleececry:'


@app.after_request
def add_security_headers(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; img-src 'self'; style-src 'self'; object-src 'none'; require-trusted-types-for 'script';"

    return response
