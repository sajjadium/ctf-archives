import binascii
import json
import os
import re
import redis

from flask import Flask
from flask import request
from flask import redirect, render_template
from flask import abort

app = Flask(__name__)
app.secret_key = os.environ.get('FLAG')

redis = redis.Redis(host='madlibbin_redis', port=6379, db=0)

generate = lambda: binascii.hexlify(os.urandom(16)).decode()
parse = lambda x: list(dict.fromkeys(re.findall(r'(?<=\{args\[)[\w\-\s]+(?=\]\})', x)))

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def create():
	tag = generate()
	template = request.form.get('template', '')
	madlib = {
		'template': template,
		'blanks': parse(template)
	}
	redis.set(tag, json.dumps(madlib))
	return redirect('/{}'.format(tag))

@app.route('/<tag>', methods=['GET'])
def view(tag):
	if redis.exists(tag):
		madlib = json.loads(redis.get(tag))
		if set(request.args.keys()) == set(madlib['blanks']):
			return render_template('result.html', stuff=madlib['template'].format(args=request.args))
		else:
			return render_template('fill.html', blanks=madlib['blanks'])
	else:
		abort(404)

if __name__ == '__main__':
	app.run()