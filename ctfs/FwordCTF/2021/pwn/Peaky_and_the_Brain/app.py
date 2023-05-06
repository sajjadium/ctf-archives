# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from PIL import Image
import subprocess
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join('static','uploads')
app.config['MAX_CONTENT_LENGTH'] = 10 * 1000
app.secret_key = os.urandom(64)

def image_to_code(file):
	colors = {(255,0,0) : '>', (0,255,0) : '.', (0,0,255) : '<', (255,255,0) : '+', (0,255,255) : '-', (255,0,188) : '[', (255,128,0) : ']', (102,0,204) : ','}
	image = Image.open(file)
	w, h = image.size
	pixels = image.load()
	code = ''
	for i in range(h):
		for j in range(w):
			p = pixels[j,i][:3]
			if p in colors:
				code += colors[p]
	return code

def interpret(code, arg):
	process = subprocess.Popen(['./interpreter', code, arg], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = process.communicate()
	return out.decode()

def save_image(file):
	im = Image.open(file)
	filename = os.urandom(20).hex()
	path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	im.save(path, format='PNG')
	return path


@app.route("/", methods=['GET', 'POST'])
def upload():
	DEFAULT_MSG = 'Pinky: Gee, Brain, what do you want to do tonight? Brain: The same thing we do every night, Pinky - try to take over the world!'
	DEFAULT_IMG = os.path.join('static', 'images/default.png')
	try:
		if request.method == 'POST':
			file = request.files.get('file')
			arg = request.form['text']
			code = image_to_code(file)
			img = save_image(file)
			out = interpret(code, arg)
			if out != '' :
				return render_template('index.html', msg=out, img=img)
			else:
				return render_template('index.html', msg=DEFAULT_MSG, img=DEFAULT_IMG)
		return render_template('index.html', msg=DEFAULT_MSG, img=DEFAULT_IMG)
	except RequestEntityTooLarge:
		return render_template('error.html', msg='File size exceeds limit.')
	except Exception as e:
		print (e)
		return render_template('error.html', msg='An error has occured.')



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=6969, debug=True)

