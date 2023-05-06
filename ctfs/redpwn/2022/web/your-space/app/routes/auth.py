from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user

from .. import db
from ..form import LoginForm, RegisterForm
from ..model import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                flash("logged in")
                next_url = request.args.get("next")
                if next_url is not None and next_url.startswith("/"):
                    return redirect(next_url)
                return redirect(url_for("main.profile"))
        else:
            flash("invalid login")
    return render_template("login.html", form=form)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("logged in")
        return redirect(url_for("main.profile"))
    return render_template("register.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    flash("logged out")
    return redirect(url_for("main.home"))
