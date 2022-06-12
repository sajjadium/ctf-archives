from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, ValidationError, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ReportForm(FlaskForm):
    url = StringField('Url', validators=[DataRequired()])
    submit = SubmitField('Fire')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class PostForm(FlaskForm):
    title = StringField('Enter your site name', validators=[DataRequired()])
    color_palette = RadioField('Choose a color palette', validators=[Length(min=1, max=140)], choices=[('#FFFFFF','white'),('#000000','black')], validate_choice=False)
    link = StringField('Enter the ID of a link', validators=[DataRequired()])
    submit = SubmitField('Generate cookie consent')