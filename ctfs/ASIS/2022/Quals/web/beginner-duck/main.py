#!/usr/bin/env python3
from flask import Flask,request,Response
import random
import re

app = Flask(__name__)
availableDucks = ['duckInABag','duckLookingAtAHacker','duckWithAFreeHugsSign']
indexTemplate = None
flag = None

@app.route('/duck')
def retDuck():
	what = request.args.get('what')
	duckInABag = './images/e146727ce27b9ed172e70d85b2da4736.jpeg'
	duckLookingAtAHacker = './images/591233537c16718427dc3c23429de172.jpeg'
	duckWithAFreeHugsSign = './images/25058ec9ffd96a8bcd4fcb28ef4ca72b.jpeg'

	if(not what or re.search(r'[^A-Za-z\.]',what)):
		return 'what?'

	with open(eval(what),'rb') as f:
		return Response(f.read(), mimetype='image/jpeg')

@app.route("/")
def index():
	return indexTemplate.replace('WHAT',random.choice(availableDucks))

with open('./index.html') as f:
	indexTemplate = f.read() 
with open('/flag.txt') as f:
	flag = f.read()

if(__name__ == '__main__'):
	app.run(port=8000)
