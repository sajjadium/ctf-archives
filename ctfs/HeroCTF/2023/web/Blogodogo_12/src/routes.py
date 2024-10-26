#!/usr/bin/env python3
from flask import (
    Blueprint,
    render_template,
    redirect,
    current_app,
    flash,
    url_for,
    request
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)
from sqlalchemy import and_

import re
import os
import subprocess

from config import db, redis_client
from src.utils import generate_hash
from src.models import Authors, Posts
from src.forms import RegisterForm, LoginForm, EditProfileForm, AddPostForm

bp_routes = Blueprint("bp_routes", __name__)


@bp_routes.route("/", methods=["GET"])
def index():
    register_number = Authors.query.count()
    posts = Posts.query.filter(Posts.draft.is_(False)).order_by(Posts.created_at).limit(5).all()
    for post in posts:
        post.author = Authors.query.filter_by(id=post.author_id).first()

    return render_template("pages/index.html", title="Index", posts=posts, register_number=register_number)

@bp_routes.route("/about", methods=["GET"])
def about():
    return render_template("pages/about.html", title="My super blog - About")

@bp_routes.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        author = Authors.query.filter_by(username=form.username.data).first()
        if author and author.verify_password(form.password.data):
            login_user(author, remember=True)

            if author.username == "admin":
                flash(os.getenv('FLAG_2'), "success")
            else:
                flash('Logged in successfully.', "success")
            return redirect(url_for('bp_routes.index'))

        flash('Wrong username or password.', "warning")

    return render_template("pages/login.html", title="Login", form=form)

@bp_routes.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.referral_code.data != current_app.config['REFERRAL_CODE']:
            flash('Wrong referral code.', "warning")
            return render_template("pages/register.html", title="Register", form=form)

        author = Authors(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(author)
        db.session.commit()
        login_user(author, remember=True)
        flash("Author registered successfully.", "success")
        return redirect(url_for('bp_routes.index'))

    return render_template("pages/register.html", title="Register", form=form)

@bp_routes.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash('Author logged out successfully.', "success")
    return redirect(url_for('bp_routes.index'))

@bp_routes.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        author = Authors.query.filter_by(id=current_user.id).first()

        _username = form.username.data
        _new_password = form.new_password.data
        _new_password_confirm = form.new_password_confirm.data
        _url = form.url.data
        _avatar = form.avatar.data

        if author.username != _username and Authors.query.filter_by(username=_username).first():
            flash("Username already exists.", "warning")
            return render_template("pages/profile.html", title="My profile", form=form)

        if _new_password and _new_password != _new_password_confirm:
            flash("The two passwords do not match", "warning")
            return render_template("pages/profile.html", title="My profile", form=form)

        author.username = _username
        author.password = _new_password
        if _url:
            author.url = _url
        if _avatar:
            author.avatar = _avatar

        db.session.add(author)
        db.session.commit()
        flash("Profile successfully edited.", "success")

    key_name_url = "profile_" + current_user.username.lower() + "_url"
    key_name_username = "profile_" + current_user.username.lower() + "_username" 

    cache_url, cache_username = redis_client.get(key_name_url), redis_client.get(key_name_username)
    if not cache_url or not cache_username:
        redis_client.set(key_name_username, current_user.username)
        redis_client.expire(key_name_username, 60)

        redis_client.set(key_name_url, current_user.url)
        redis_client.expire(key_name_url, 60)

    cache_url, cache_username = redis_client.get(key_name_url).decode(), redis_client.get(key_name_username).decode()
    return render_template("pages/profile.html", title="My profile", form=form,
        cache_url=cache_url, cache_username=cache_username)

@bp_routes.route("/add", methods=["GET", "POST"])
@login_required
def add_post():
    form = AddPostForm()
    if form.validate_on_submit():
        result = Posts.query.filter_by(slug=form.slug.data).first()
        if result:
            flash("Slug already exists.", "warning")
            return redirect(url_for('bp_routes.add_post')) 

        post = Posts(
            title=form.title.data,
            subtitle=form.subtitle.data,
            slug=form.slug.data,
            content=form.content.data,
            draft=True,
            hash_preview=generate_hash(),
            author_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash("Post successfully added.", "success")
        return redirect(url_for('bp_routes.view_post', slug=post.slug))

    return render_template("pages/add_post.html", title="Add a post", form=form)

@bp_routes.route("/post/<string:slug>", methods=["GET"])
def view_post(slug):
    post = Posts.query.filter(Posts.slug == slug).first()

    if not post:
        flash("This post does not exists.", "warning")
        return redirect(url_for('bp_routes.index')) 

    if post.draft and (not current_user.is_authenticated or post.author_id != current_user.id):
        flash("You cannot see draft of other users.", "warning")
        return redirect(url_for('bp_routes.index')) 

    author = Authors.query.filter_by(id=post.author_id).first()
    return render_template("pages/post.html", title="View a post", post=post, author=author)

@bp_routes.route("/post/report", methods=["POST"])
def report_post():
    url = request.form.get("url", "")

    if not re.match("^http://localhost:5000/.*", url):
        flash("URL not valid, please match: ^http://localhost:5000/.*", "warning")
        return redirect(url_for('bp_routes.index'))

    subprocess.run(["node", "/app/bot/bot.js", url])
    flash("Your request has been sent to an administrator!", "success")
    return redirect(url_for('bp_routes.index'))

@bp_routes.route("/post/preview/<string:hash_preview>", methods=["GET"])
def preview_post(hash_preview):
    post = Posts.query.filter_by(hash_preview=hash_preview).first()

    if post:
        author = Authors.query.filter_by(id=post.author_id).first()
        return render_template("pages/post.html", title="Preview a post", post=post, author=author)

    flash("Unable to find the corresponding post.", "warning")
    return redirect(url_for('bp_routes.index'))

@bp_routes.route("/author/<int:author_id>", methods=["GET"])
def view_author(author_id):
    author = Authors.query.filter_by(id=author_id).first()

    if author:
        posts = Posts.query.filter_by(author_id=author.id).all()
        return render_template("pages/author.html", title="Author profile", author=author, posts=posts)

    flash("Unable to find the corresponding author.", "warning")
    return redirect(url_for('bp_routes.index'))
