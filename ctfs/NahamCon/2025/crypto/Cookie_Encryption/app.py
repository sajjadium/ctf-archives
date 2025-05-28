import requests
from flask import Flask, render_template, request, session, redirect, abort, url_for, make_response
from models import db, Users
from sqlalchemy_utils import database_exists
from sqlalchemy.exc import OperationalError
from encryption import encrypt, decrypt
 
app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

def authed():
	return bool(session.get('id', False))

with app.app_context():
	if database_exists(app.config['SQLALCHEMY_DATABASE_URI']) is False:
		try:
			db.create_all()
		except OperationalError:
			pass
		admin = Users.query.filter_by(username='admin').first()
		if admin is None:
			admin = Users('admin', 'admin')
			admin.password = 'admin'
			db.session.add(admin)
			db.session.commit()

@app.context_processor
def inject_user():
	if session:
		return dict(session)
	return dict()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	else:
		username = request.form.get('username').strip()
		password = request.form.get('password').strip()
		errors = []
		user = Users.query.filter_by(username=username).first()
		if user:
			if user.password == password:
				session['id'] = user.id
				session['username'] = user.username
				resp = make_response(redirect('/'))
				if session['username'] != "admin":
					resp.set_cookie('secret',encrypt(b"This is not the admin secret!").hex())
				else:
					resp.set_cookie('secret',encrypt(app.config.get("FLAG")).hex())
				return resp
			else:
				errors.append("That password doesn't match what we have")
				return render_template('login.html', errors=errors)
		else:
			errors.append("Couldn't find a user with that username")
			return render_template('login.html', errors=errors)

			
@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	else:
		username = request.form.get('username').strip()
		password = request.form.get('password').strip()
		confirm = request.form.get('confirm').strip()
		errors = []
		if password != confirm:
			errors.append('Your passwords do not match')
		if len(password) < 5:
			errors.append('Your password must be longer')
		exists = Users.query.filter_by(username=username).first()
		if exists:
			errors.append('That username is taken')
		if errors:
			return render_template('register.html', username=username, errors=errors)
		user = Users(username, password)
		db.session.add(user)
		db.session.commit()
		db.session.flush()
		session['id'] = user.id
		session['username'] = user.username
		db.session.close()
		resp = make_response(redirect('/'))
		resp.set_cookie('secret',encrypt(b"This is not the admin secret!").hex())
		return resp

@app.route('/cookie', methods=['GET'])
def cookie_checker():
	if not authed():
		return redirect('/login')
	else:
		secret = decrypt(bytearray.fromhex(request.cookies.get('secret')))
		if b"Error" not in secret:
			resp = make_response("The secret is all good!")
		else:
			resp = make_response("The secret is not all good!")
		return resp

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)