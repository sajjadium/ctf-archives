from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from flask_wtf.csrf import generate_csrf
from models import User
from server import app, db, login_manager
from sqlalchemy.orm import Session
from werkzeug.datastructures import ImmutableMultiDict
from wtforms import (BooleanField, PasswordField, StringField, SubmitField,
                     validators)

from flask import Blueprint, jsonify, redirect, render_template, request

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(user_id):
    with db.Session(db.engine) as session:
        return session.execute(db.select(User).filter(
            User.id == user_id)).scalars().one_or_none()


@auth.route("/csrf", methods=["GET"])
def csrf():
    return jsonify({"csrfToken": generate_csrf()}), 200


def str_form_errors(form_errors):
    str_errors = []
    for k, errors in form_errors.items():
        if k is None:
            k = "Error"
        for error in errors:
            str_errors.append(f"{k}: {error}")
    return ", ".join(str_errors)


class LoginForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[
            validators.InputRequired(),
        ],
        id="username",
        default="user",
        name="username",
    )
    password = PasswordField(
        label="Password",
        validators=[
            validators.InputRequired(),
        ],
        id="password",
        default="password",
        name="password",
    )
    remember_me = BooleanField(
        label="Remember me",
        id="remember_me",
        default=False,
        name="remember_me",
    )
    submit = SubmitField(
        label="Login",
        id="submit",
        name="submit",
    )

    _fail_message = "Wrong credentials"

    def validate(self, extra_validators=None):
        if not super().validate(extra_validators=extra_validators):
            return False
        with db.Session(db.engine) as session:
            self._user = session.execute(db.select(User).filter(
                User.username == self.username.data)).scalars().one_or_none()
        if self._user is None:
            self.form_errors.append(self._fail_message)
            return False
        if not self._user.verify(self.password.data):
            self.form_errors.append(self._fail_message)
            return False
        return True


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginForm()
    if form.validate_on_submit():
        login_user(form._user, remember=form.remember_me.data)
        return redirect("/")
    return render_template("login.html", form=form)


login_manager.login_view = "auth.login"


def username_does_not_exist_validator(form, field):
    if User.exists(username=field.data):
        raise validators.ValidationError("username already exists")
    return True


class RegisterForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            validators.DataRequired(),
            validators.Length(min=3),
            username_does_not_exist_validator,
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=8),
        ]
    )
    confirm = PasswordField(
        "Repeat password",
        validators=[
            validators.DataRequired(),
            validators.EqualTo("password", message="passwords do not match"),
        ]
    )
    submit = SubmitField(
        label="Submit",
        id="submit",
        name="submit",
    )


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        User.register(
            username=form.username.data,
            password=form.password.data,
        )
        return redirect("/")
    return render_template("register.html", form=form)


@auth.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"ok": True}), 200


# @login_manager.unauthorized_handler
# def unauthorized():
#     return abort(401)
