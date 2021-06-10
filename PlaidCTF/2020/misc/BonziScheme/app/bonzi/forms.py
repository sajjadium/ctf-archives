from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileAllowed, FileRequired
from flask_wtf.recaptcha import RecaptchaField
from wtforms import IntegerField, SubmitField, FileField
from wtforms.validators import DataRequired, InputRequired, NumberRange

class ACSSubmitForm(FlaskForm):
    acsfile = FileField("ACS File", validators=[InputRequired(), FileRequired(), FileAllowed(["acs"], "Only ACS files allowed")])
    imgidx = IntegerField("Favorite Number", validators=[InputRequired(), NumberRange(0, 1999, "Maximum of 2000 images in ACS file supported")])
    recaptcha = RecaptchaField()
    submit = SubmitField("Upload")
