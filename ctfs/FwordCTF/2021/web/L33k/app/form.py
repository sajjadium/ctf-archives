from flask_wtf import Form, RecaptchaField
from wtforms import StringField, validators

class ReportForm(Form):   
	url = StringField('Url To Visit', [validators.DataRequired(), validators.Length(max=255)],render_kw={"placeholder": "http://URL/"})
	recaptcha = RecaptchaField()
