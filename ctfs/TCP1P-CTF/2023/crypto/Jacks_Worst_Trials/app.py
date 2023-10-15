# flask imports
from flask import Flask, request, jsonify, make_response, render_template, redirect, url_for, flash, Response, send_file
from flask_sqlalchemy import SQLAlchemy
import uuid # for public id
from werkzeug.security import generate_password_hash, check_password_hash

import jwt 
from datetime import datetime, timedelta
from functools import wraps
from Crypto.PublicKey import RSA


# creates Flask object
app = Flask(__name__)
with open('challengefiles/private_key.pem', 'rb') as f:
   PRIVATE_KEY = f.read()
with open('challengefiles/public_key.pem', 'rb') as f:
   PUBLIC_KEY = f.read()

# configuration
# NEVER HARDCODE YOUR CONFIGURATION IN YOUR CODE
# INSTEAD CREATE A .env FILE AND STORE IN IT
app.config['SECRET_KEY'] = 'OFCOURSETHISISNOTHEREALSECRETKEYBOI'
# database name
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# creates SQLALCHEMY object
db = SQLAlchemy(app)

# Database ORMs
class User(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	public_id = db.Column(db.String(50), unique = True)
	name = db.Column(db.String(100))
	email = db.Column(db.String(70), unique = True)
	password = db.Column(db.String(80))

# decorator for verifying the JWT
def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		if 'token' in request.cookies:
			token = request.cookies.get('token')
		# return to login if token is not passed
		if not token:
			return make_response(redirect(url_for('login')))

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, PUBLIC_KEY)
			current_user = User.query\
				.filter_by(public_id = data['public_id'])\
				.first()
		except Exception as e:
			flash('Invalid or expired token')
			return make_response(render_template('error.html'), 401)
		if "admin" in data and data["admin"]:
			flash('Welcome, Admin. Here\'s your flag: TCP1P{REDACTED}')
			return make_response(render_template('admin.html'))
		return f(current_user, *args, **kwargs)

	return decorated

@app.route('/', methods =['GET'])
def index():
	return render_template('index.html')

@app.route('/main', methods =['GET'])
@token_required
def mainpage(current_user):
	flash(f'hello, {current_user.name}')
	return render_template('main.html')

# @app.route('/public_key.pem')
# @token_required
# def downloadFile (current_user):
#     path = "challengefiles/public_key.pem"
#     return send_file(path, as_attachment=True)

# route for logging user in
@app.route('/login', methods=['GET', 'POST'])
def login():
	# creates dictionary of form data
	if request.method=='GET': # if the request is a GET we return the login page
		return render_template('login.html')
	else:
		auth = request.form

		if not auth or not auth.get('email') or not auth.get('password'):
			# returns 401 if any email or / and password is missing
			flash('Email or password cannot be empty.')
			return make_response(redirect(url_for('login')))#401

		user = User.query\
			.filter_by(email = auth.get('email'))\
			.first()

		if not user:
			# returns 401 if user does not exist
			flash('Please check your login details and try again.')
			return make_response(redirect(url_for('login')))#401

		if check_password_hash(user.password, auth.get('password')):
			# generates the JWT Token
			token = jwt.encode({
				'public_id': user.public_id,
				'name': user.name,
				'admin': False,
				'exp' : datetime.utcnow() + timedelta(minutes = 5)
			}, PRIVATE_KEY, algorithm='RS256')
			response = make_response(redirect(url_for('mainpage')))#201
			response.set_cookie('token', token)
			return response
		# returns 403 if password is wrong
		flash('Please check your login details and try again.')
		return make_response(redirect(url_for('login')))#403

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if request.method=='GET': # if the request is a GET we return the login page
		return render_template('signup.html')
	else:
		# creates a dictionary of the form data
		data = request.form

		# gets name, email and password
		name, email = data.get('name'), data.get('email')
		password = data.get('password')
		if not data or not email or not password or not name:
			# returns 401 if any email or / and password is missing
			flash('Email, name, or password cannot be empty.')
			return make_response(redirect(url_for('signup')))#401

		# checking for existing user
		user = User.query\
			.filter_by(email = email)\
			.first()
		if not user:
			# database ORM object
			user = User(
				public_id = str(uuid.uuid4()),
				name = name,
				email = email,
				password = generate_password_hash(password)
			)
			# insert user
			db.session.add(user)
			db.session.commit()

			# return make_response('Successfully registered.', 201)
			flash('Successfully registered')
			return make_response(redirect(url_for('login')))#401
		else:
			# returns 202 if user already exists
			# return make_response('User already exists. Please Log in.', 202)
			flash('User already exists. Please Log in.')
			return make_response(redirect(url_for('login')))

@app.route('/logout') # define logout path
# @token_required
def logout(): #define the logout function
	response = make_response(redirect(url_for('index')))#201
	response.delete_cookie('token')
	return response

if __name__ == "__main__":
	# setting debug to True enables hot reload
	# and also provides a debuger shell
	# if you hit an error while running the server
	app.run(host = '0.0.0.0',port = 5000, debug = False)
