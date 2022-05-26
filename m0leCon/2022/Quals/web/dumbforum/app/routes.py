from flask import render_template, render_template_string, flash, redirect, url_for, abort
from app import db, app
from flask_login import current_user, login_user
from app.models import User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse, url_decode
import calendar
from app.forms import RegistrationForm
from flask_login import logout_user
from urllib.parse import unquote
from datetime import datetime

from app.forms import LoginForm, PostForm, EditProfileForm

from app.models import Post


ROWS_PER_PAGE = 7
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route("/")
def index():
    return redirect(url_for('forums'))


@app.route("/forums",methods=['GET'])
def forums():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,ROWS_PER_PAGE,error_out=False)
    no_post_flag = False
    for post in posts.items:
        post.month_name = calendar.month_name[post.timestamp.month]
    if len(posts.items) == 0:
        no_post_flag = True
    return render_template('forums.html', posts = posts, no_post_flag = no_post_flag)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/post', methods=['GET', 'POST'])
def post():
    if current_user.is_authenticated:
        form = PostForm()
        form.username.data = current_user.username
        form.data["username"] = current_user.username
        if form.validate_on_submit():
            post = Post(username = current_user.username, title = form.title.data, body = form.body.data)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('forums'))
    else:
        return redirect(url_for('login'))
    return render_template('post.html', title='Post', form=form)
 



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    with open('app/templates/profile.html') as p:
        profile_html = p.read()
    
    profile_html = profile_html % (current_user.username, current_user.email, current_user.about_me)

    if(current_user.about_me == None):
        current_user.about_me = ""
    return render_template_string(profile_html)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('forums'))

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)


    if request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        return render_template('edit_profile.html', title='Edit Profile', form=form)
    else:
        if form.validate_on_submit():
            posts = Post.query.filter_by(username=current_user.username)
            for post in posts:
                post.username = form.username.data
            current_user.username = form.username.data
            current_user.about_me = form.about_me.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('profile'))
        else:
            render_template('edit_profile.html', title='Edit Profile', form=form)
