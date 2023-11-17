from flask import Flask,request,render_template,session,redirect
import uuid
from passlib.hash import pbkdf2_sha256
from app import db

class User:
	def signup(self):
		user = {
		"_id":uuid.uuid4().hex,
		"username":request.form['form_username'],
		"password":pbkdf2_sha256.encrypt(request.form['form_password'])
		}

		if db.users.find_one({"username":user['username']}):
			return render_template('register.html',error="username already exist"),400
		if db.users.insert_one(user):
			return self.handle_session(user)

		return render_template('register.html',error="some error occured while signing up"),400	

	def handle_session(self,user):
		del user['password']
		session['user'] = user
		return redirect('/')

	def signin(self):
		user = db.users.find_one({
			"username":request.form['form_username']
			})
		if user:
			pwd = pbkdf2_sha256.verify(request.form['form_password'],user['password'])
			if pwd == True:
				return self.handle_session(user)
			else:
				return render_template('login.html',error="please enter the correct password"),400
		elif user == None:
			return render_template('login.html',error="no user in that name"),400

		return render_template('login.html',error="some error occured while signing up"),400
