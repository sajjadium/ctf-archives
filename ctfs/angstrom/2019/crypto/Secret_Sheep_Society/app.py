from flask import Flask
from flask import request
from flask import redirect, render_template

from .secret import flag, key
from .manager import Manager

app = Flask(__name__)
manager = Manager(key)

@app.route('/')
def index():
	try:
		token = request.cookies.get('token')
		session = manager.unpack(token)
		return render_template('index.html', session=session, flag=flag)
	except:
		pass
	return render_template('index.html')

@app.route('/enter', methods=['POST'])
def enter():
	handle = request.form.get('handle')
	session = {
		'admin': False,
		'handle': handle
	}
	token = manager.pack(session)
	response = redirect('/')
	response.set_cookie('token', token)
	return response

@app.route('/exit', methods=['POST'])
def exit():
	response = redirect('/')
	response.set_cookie('token', expires=0)
	return response

if __name__ == "__main__":
	app.run()