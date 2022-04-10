from flask_wtf import Form, RecaptchaField
from wtforms import StringField, validators,PasswordField,SubmitField

class ReportForm(Form):   
	url = StringField('Url To Visit', [validators.DataRequired(), validators.Length(max=255)],render_kw={"placeholder": "http://URL/"})
	recaptcha = RecaptchaField()
class LoginForm(Form):
	user_name  = StringField('userName', validators=[validators.DataRequired()])
	password = PasswordField('password', validators=[validators.DataRequired()])
	submit = SubmitField('Sign In')
class RegisterForm(Form):
	user_name  = StringField('userName', validators=[validators.DataRequired()])
	password = PasswordField('password', validators=[validators.DataRequired()])
	submit = SubmitField('Sign Up')

