import os
from uuid import uuid4
from datetime import datetime
from functools import wraps
from flask import (
    render_template, request, redirect, url_for, session, flash, send_file,
    current_app as app, jsonify, g, abort
)

from .models import User, BlogPost
from .helpers import (
    allowed_username, allowed_file, gen_filename, ensure_upload_directory,
)
from . import db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_get'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/status', methods=['GET'])
def status():
    current_time = datetime.now()
    uptime = current_time - app.config['START_TIME']
    return jsonify({"status": "ok", "server_time": str(current_time), "uptime": str(uptime)})
@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        my_posts = BlogPost.query.filter_by(user_id=user.id).all()
    else:
        user = None
        my_posts = []

    posts = BlogPost.query.filter_by(visibility=True).join(User).add_columns(
        BlogPost.id,
        BlogPost.uuid,
        BlogPost.title,
        User.username,
        User.profile_photo
    ).all()

    return render_template('index.html', user=user, posts=posts, my_posts=my_posts)

@app.route('/post/<uuid>', methods=['GET'])
def view_post(uuid):
    post = BlogPost.query.filter_by(uuid=uuid).first_or_404()
    if post.user_id != session.get('user_id') and not post.visibility:
        abort(404)
    author = User.query.get(post.user_id)
    return render_template('view_post.html', post=post, author=author)

@app.route('/register', methods=['GET'])
def register_get():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register_post():
    username = request.form['username']
    if not allowed_username(username):
        flash('Invalid username', 'error')
        return redirect(url_for('register_get'))
    password = request.form['password']
    if User.query.filter_by(username=username).first():
        flash('Username already exists', 'error')
        return redirect(url_for('register_get'))
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    flash('Registration successful', 'success')
    return redirect(url_for('login_get'))

@app.route('/login', methods=['GET'])
def login_get():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        flash('Login successful', 'success')
        return redirect(url_for('index'))
    flash('Invalid credentials', 'error')
    return redirect(url_for('login_get'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('login_get'))

@app.route('/profile_picture', methods=['GET'])
def profile_picture():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if user is None:
        return "User not found", 404
    if user.profile_photo is None:
        return send_file(os.path.join(app.static_folder, 'default.png'))
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], user.username + user.profile_photo)
    if not os.path.exists(file_path):
        return send_file(os.path.join(app.static_folder, 'default.png'))
    return send_file(file_path)

@app.route('/profile', methods=['GET'])
@login_required
def profile_get():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/profile', methods=['POST'])
@login_required
def profile_post():
    user = User.query.get(session['user_id'])
    about_me = request.form.get('about_me')
    if about_me is not None:
        user.about_me = about_me
    file = request.files.get('profile_photo')
    if file:
        user.profile_photo = None
        user_directory = ensure_upload_directory(app.config['UPLOAD_FOLDER'], user.username)
        if not user_directory:
            flash('Failed to create user directory', 'error')
            return redirect(url_for('profile_get'))
        ext = os.path.splitext(file.filename)[1].lower()
        save_filename = f"{gen_filename(file.filename, user.username)}{ext}"
        if not allowed_file(save_filename):
            flash('Invalid file type', 'error')
            return redirect(url_for('profile_get'))
        filepath = os.path.join(user_directory, save_filename)
        if not os.path.exists(filepath):
            try:
                user.profile_photo = "/"+save_filename
                file.save(filepath)
            except:
                user.profile_photo = ''
                flash('Failed to save file', 'error')
                return redirect(url_for('profile_get'))
            finally:
                db.session.commit()
        else:
            flash('File already exists', 'error')
            return redirect(url_for('profile_get'))
    db.session.commit()
    flash('Profile updated successfully', 'success')
    return redirect(url_for('profile_get'))
@app.route('/new_post', methods=['GET'])
@login_required
def new_post_get():
    return render_template('new_post.html')

@app.route('/new_post', methods=['POST'])
@login_required
def new_post_post():
    title = request.form['title']
    content = request.form['content']
    visibility = request.form.get('visibility') == 'on'
    post = BlogPost(uuid=str(uuid4()), title=title, content=content, visibility=visibility, user_id=session['user_id'])
    db.session.add(post)
    db.session.commit()
    flash('Post created successfully', 'success')
    return redirect(url_for('index'))
