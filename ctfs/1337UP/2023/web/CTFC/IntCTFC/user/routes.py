from flask import Flask,render_template
from app import app
from user.models import User

@app.route('/user/signup',methods=['POST'])
def signup():
	try:
		return User().signup()
	except KeyError:
		return render_template('register.html',error="dont try to hack!!"),406

@app.route('/user/signin',methods=['POST'])
def signin():
	try:
		return User().signin()
	except KeyError:
		return render_template('login.html',error="dont try to hack!!"),406