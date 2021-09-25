#!/usr/bin/python3

import os
from requests import get
from base64 import b64encode, b64decode
from flask import Flask, request, render_template

app = Flask(__name__)

class JSON(object):
	def __init__(self):
		self.forbidden = ["'","\"","{","}","[","]",",","(",")","\\",";","%"]
		self.checked = []

	def _forbidden_chk(self, key, value):
		chk = False
		for bad in self.forbidden:
			if bad in key:
				chk = True
				break
			if bad in value:
				chk = True
				break
		return chk

	def _checked(self, key):
		chk = True
		if key in self.checked:
			chk = False
		return chk

	def _security(self, key, value):
		chk = False
		if not self._checked(key):
			return chk
		if self._forbidden_chk(key, value):
			chk = True
		if key == "img":
			value = b64decode(bytes(value,'utf-8')).decode()
			if self._forbidden_chk(key, value):
				chk = True
		if chk == False:
			self.checked.append(key)
		return chk

	def parse(self, data):
		parsed_data =  [obj.replace("'",'').replace('"','').split(':') for obj in data.decode()[1:][:-1].split(',')]
		built_data = {}
		for obj in parsed_data:
			if self._security(obj[0], obj[1]):
				return "Jasons Secure JSON Parsing Blocked Your Request"
			if obj[0] == "img":
				obj[1] = b64decode(bytes(obj[1],'utf-8')).decode()
			built_data[obj[0]] = obj[1]
		return built_data
		
def get_as_b64(img):
	try:
		if img.startswith('http://127.0.0.1/static/images/'):
			return b64encode(get("http://127.0.0.1:9097/"+img).content).decode()
		return None
	except Exception as e:
		return None

@app.route('/')
def _index():
	return render_template('index.html')


@app.route('/jason_loader', methods=['POST'])
def _app_jason_loader():
	if request.headers.get('Content-Type') != 'application/json':
		return '{"error": "invalid content type"}', 400
	json = JSON()
	pdata = json.parse(request.data)
	if type(pdata) == str:
		return "{\"error\": \""+pdata+"\"}"
	img = pdata.get('img')
	if not img:
		return "{\"error\": \"Jasons JSON Security Module Triggered\"}"
	imgdata = '{"imagedata": "' + get_as_b64(img) + '"}' 
	return imgdata, 200

@app.route('/admin/flag')
def _flag():
	if request.remote_addr != "127.0.0.1":
		return "Unauthorized.", 401
	return str(os.environ.get('FLAG')), 200


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80,debug=False)

