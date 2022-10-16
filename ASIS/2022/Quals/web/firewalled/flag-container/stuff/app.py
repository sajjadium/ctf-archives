#!/usr/bin/env python3
from flask import Flask,request
import requests
import json
import os

app = Flask(__name__)
application = app
flag = os.environ.get('FLAG')

@app.route('/flag')
def index():
	args = request.args.get('args')

	try:
		r = requests.post('http://firewalled-curl/req',json=json.loads(args)).json()
		if('request' in r and 'flag' in r['request'] and 'flag' in request.headers['X-Request']):
			return flag
	except:
		pass
	return 'No flag for you :('

if(__name__ == '__main__'):
	app.run(port=8000)