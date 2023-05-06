from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import InputRequired, Length

from .model import User


def validate_username(_form, field):
    if User.query.filter_by(username=field.data).count():
        raise ValidationError("username is taken")


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired("username is required")]
    )
    password = PasswordField(
        "password", validators=[InputRequired("password is required")]
    )
    submit = SubmitField("login")


class RegisterForm(FlaskForm):
    username = StringField(
        "username",
        validators=[
            InputRequired("username is required"),
            Length(max=32, message="username too long"),
            validate_username,
        ],
    )
    password = PasswordField(
        "password", validators=[InputRequired("password is required")]
    )
    submit = SubmitField("register")


class SpaceForm(FlaskForm):
    name = StringField(
        "name",
        validators=[
            InputRequired("name is required"),
            Length(max=32, message="name too long"),
        ],
    )
    submit = SubmitField("create")


class WebhookForm(FlaskForm):
    webhook = StringField(
        "webhook",
        validators=[
            InputRequired("webhook is required"),
            Length(max=96, message="webhook too long"),
        ],
    )
    submit = SubmitField("update")


class PostForm(FlaskForm):
    content = TextAreaField("content")
    submit = SubmitField("post")
