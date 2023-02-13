from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from sqlalchemy import or_, text

from app import app, db
from .models import Post, Image
from .utils import serialize_image, deserialize_images
import os

MAX_IMAGE_SIZE = 1000000

limiter = Limiter (
    get_remote_address,
    app=app,
    default_limits=["360 per hour"],
    storage_uri="memory://",
)


@app.route('/')
def home():
    posts = db.session.query(Post).filter(Post.active == True).all()
    return render_template('home.html', posts=posts[::-1])


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/posts', methods=['GET'])
def post():
    p = db.session.query(Post).get(request.args['post_id'])
    if p == None:
        flash('invalid post')
        return redirect(url_for('home'))

    images = deserialize_images(p)
    return render_template('post.html', post=p, images=images)

@app.route('/search')
def search():
    if 'search-query' not in request.args:
        return render_template('search.html', results=[])

    query = request.args['search-query']
    results = db.session.query(Post)\
        .filter(or_(Post.content.contains(query), Post.title.contains(query)))\
        .filter(Post.active).all()

    return render_template('search.html', results=results)


@app.route('/image-search', methods=['GET', 'POST'])
def image_search():
    if 'image-query' not in request.files or request.method == 'GET':
        return render_template('image-search.html', results=[])

    incoming_file = request.files['image-query']
    size = os.fstat(incoming_file.fileno()).st_size
    if size > MAX_IMAGE_SIZE:
        flash("image is too large (50kb max)");
        return redirect(url_for('home'))

    spic = serialize_image(incoming_file.read())

    try:
        res = db.session.connection().execute(\
            text("select parent as PID from images where b85_image = '{}' AND ((select active from posts where id=PID) = TRUE)".format(spic)))
    except Exception:
        return ("SQL error encountered", 500)

    results = []
    for row in res:
        post = db.session.query(Post).get(row[0])
        if (post not in results):
            results.append(post)

    return render_template('image-search.html', results=results)


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
