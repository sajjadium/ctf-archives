from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import SubmitField, FileField
from wtforms.validators import InputRequired
from markupsafe import Markup
from flask_wtf.recaptcha import RecaptchaField


class AppFileForm(FlaskForm):
    myfile = FileField("File", validators=[InputRequired(), FileRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField("Upload")