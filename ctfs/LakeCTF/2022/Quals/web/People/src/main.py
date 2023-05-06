from flask import Blueprint, abort
from flask import flash, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from . import db, admin_token, limiter, q
from .models import User
from .bot import visit

main = Blueprint('main', __name__)


@main.route('/login')
def login():
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('main.login'))

    login_user(user)
    return redirect(url_for('main.profile'))


@main.route('/signup')
def signup():
    return render_template('form.html', edit=False)


@main.route('/signup', methods=['POST'])
@limiter.limit("4/minute")
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    fullname = request.form.get('fullname')
    title = request.form.get('title')
    lab = request.form.get('lab')
    bio = request.form.get('bio')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists', 'danger')
        return redirect(url_for('main.signup'))

    new_user = User(id=secrets.token_hex(16),
                    email=email,
                    password=generate_password_hash(password),
                    fullname=fullname,
                    title=title,
                    lab=lab,
                    bio=bio)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return redirect(url_for('main.profile'))


@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    else:
        return redirect(url_for('main.signup'))


@main.route('/profile', defaults={'user_id': None})
@main.route('/profile/<user_id>')
def profile(user_id):
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            abort(404)
    elif current_user.is_authenticated:
        user = current_user
    else:
        return redirect(url_for('main.login'))

    return render_template('profile.html', user=user, own_profile=user == current_user)


@main.route('/edit')
@login_required
def edit():
    return render_template('form.html', edit=True,
                           email=current_user.email,
                           fullname=current_user.fullname,
                           title=current_user.title,
                           lab=current_user.lab,
                           bio=current_user.bio)


@main.route('/edit', methods=['POST'])
@login_required
def edit_post():
    User.query.filter_by(id=current_user.id).update({
        'fullname': request.form.get('fullname'),
        'title': request.form.get('title'),
        'lab': request.form.get('lab'),
        'bio': request.form.get('bio')
    })
    db.session.commit()

    return redirect(url_for('main.profile'))


@main.route('/flag')
def flag():
    if request.cookies.get('admin_token') == admin_token:
        return os.getenv('FLAG') or 'flag{flag_not_set}'
    else:
        abort(403)


@main.route('/report/<user_id>', methods=['POST'])
@limiter.limit("2/2 minute")
def report(user_id):
    user = User.query.get(user_id)
    q.enqueue(visit, user.id, admin_token)
    flash("Thank you, an admin will review your report shortly.", "success")
    return redirect(url_for('main.profile', user_id=user_id))
