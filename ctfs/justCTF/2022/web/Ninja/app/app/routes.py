from flask import render_template, request, redirect, flash, url_for
from app import app, db
from app.models import Consent, User
from flask_login import login_user, logout_user, current_user, login_required
from .form import LoginForm, RegistrationForm, PostForm, ReportForm
from app import login_manager
from app import limiter
import logging
import os
import requests

login_manager.init_app(app)

STATIC = os.environ.get('BASE_URL', "http://127.0.0.1:5000") + "/static/"
BOT = os.environ.get('BOT_URL') or "http://127.0.0.1:8000/"


@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Content-Security-Policy'] = f"default-src 'none'; font-src {STATIC}; form-action 'self'; object-src 'none'; script-src {STATIC}; base-uri 'none'; style-src {STATIC} 'unsafe-inline'; img-src * data:;"
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consents', methods=['GET', 'POST'])
@login_required
def consents():
    form = PostForm()
    if form.validate_on_submit():
        post = Consent(title=form.title.data, color_palette=form.color_palette.data, link=form.link.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your consent is now live!')
        return redirect(url_for('consents'))
    entries = current_user.consents.all()
    return render_template('consents.html', consents=entries, form=form)

@app.route('/consent/<int:id>', methods=['GET'])
@login_required
def consent(id):
    if not id or id != 0:
        if current_user.id == 1:
            entry = Consent.query.filter_by(id=id).first()
        else:
            entry = Consent.query.filter_by(id=id, id_user=current_user.id).first()
        return render_template('consent.html', consent=entry, link=request.args.get("link")) if entry else redirect('/')
    else:
        return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/report', methods=['GET', 'POST'])
@limiter.limit("1 per minute", methods=['POST'])
def report():
    form = ReportForm()
    if form.validate_on_submit():
        requests.get(BOT, params={"url":form.url.data})
    return render_template('report.html', title='Report', form=form)

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
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per minute", methods=['POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
