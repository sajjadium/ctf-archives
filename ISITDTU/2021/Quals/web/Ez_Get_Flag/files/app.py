from flask import Flask, render_template, render_template_string, url_for, redirect, session, request
from lib import sql, waf,captcha

app = Flask(__name__)
app.config['SECRET_KEY'] = '[CENSORED]'

HOST = '0.0.0.0'
PORT = '5000'

@app.route('/')
def index():
	if 'username' in session:
		return redirect(url_for('home'))
	return redirect(url_for('login'))

@app.route('/home')
def home():
	if 'username' in session:
		secret = session['sr']
		return render_template('home.html', secret=secret)
	return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
	if 'username' in session:
		return redirect(url_for('home'))
	else:
		if request.method == "POST":
			username, password = '', ''
			username = request.form['username']
			password = request.form['password']
			if sql.login_check(username,password) > 0 and username == 'admin':
				session['username'] = 'admin'
				session['check'] = 1
				return render_template('home.html')
			else:
				cc, secret = '', ''
				cc = request.form['captcha']
				secret = request.form['secret']
				if captcha.check_captcha(cc):
					session['username'] = 'guest'
					session['check'] = 0
					session['sr'] = secret
					return redirect(url_for('home'))
			return render_template('login.html', msg='Ohhhh Noo - Incorrect !')
		return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
	if 'usename' in session:
		return redirect(url_for('home'))
	else:
		if request.method == "POST":
			username, password = '', ''
			username = request.form['username']
			password = request.form['password']
			if waf.valid_register(username,password):
				sql.reg(username,password)
				return redirect(url_for('login'))
			return render_template('register.html', msg='Registration failed !')
		return render_template('register.html')

@app.route('/rate',methods=['GET','POST'])
def rate():
	if 'username' not in session:
		return redirect(url_for('login'))
	else:
		if request.method == "POST":
			picture = ''
			picture = request.form['picture']
			if session['username'] == 'admin' and session['check'] == 1:
				picture = picture.replace('{{','{').replace('}}','}').replace('>','').replace('#','').replace('<','')
				if waf.isValid(picture):
					render_template_string(picture)
				return 'you are admin you can choose all :)'
			else:
				_waf = ['{{','+','~','"','_','|','\\','[',']','#','>','<','!','config','==','}}']
				for char in _waf:
					if char in picture:
						picture = picture.replace(char,'')
				if waf.check_len(picture):
					render_template_string(picture)
				return 'you are wonderful ♥'
		return render_template('rate.html')
	return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(HOST,PORT)