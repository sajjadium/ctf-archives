from wtforms import *

class AccountForm(Form):
	username = StringField(validators=[validators.InputRequired()])
	password = StringField(validators=[validators.InputRequired()])

class TaskForm(Form):
	title = StringField(validators=[validators.InputRequired()])
	content = StringField(validators=[validators.InputRequired()])
	priority = IntegerField(validators=[validators.InputRequired()])

class EditForm(Form):
	title = StringField(validators=[validators.Optional()])
	content = StringField(validators=[validators.Optional()])
	priority = IntegerField(validators=[validators.Optional()])
