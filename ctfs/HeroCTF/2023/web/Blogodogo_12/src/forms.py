from flask_wtf import FlaskForm
from wtforms import (
    PasswordField,
    StringField,
    BooleanField,
    TextAreaField,
    FileField,
    SubmitField,
    ValidationError
)
from wtforms.validators import DataRequired, EqualTo

from src.models import Authors

from re import search as re_search


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Password", validators=[DataRequired(), EqualTo("confirm_password")]
    )
    confirm_password = PasswordField("Confirm Password")
    referral_code = StringField("ReferralCode", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_username(self, field):
        if Authors.query.filter_by(username=field.data).first():
            raise ValidationError("Username is already in use.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    old_password = PasswordField("Old password")
    new_password = PasswordField("New password",
                                validators=[EqualTo("new_password_confirm")])
    new_password_confirm = PasswordField("Confirm the new password")
    url = StringField("External link")
    avatar = FileField("Upload avatar")
    submit = SubmitField("Edit profile")


class AddPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    slug = StringField('Slug', validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Add a post")

    def validate_slug(self, field):
        if not re_search(r"^[a-z0-9-]+$", field.data):
            raise validators.ValidationError('Invalid slug format.')
