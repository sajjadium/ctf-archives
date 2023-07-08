import os
import sqlite3
import subprocess

from flask import Flask, request, render_template

app = Flask(__name__)

@app.get('/')
def index():
	sequence = request.args.get('sequence', None)
	if sequence is None:
		return render_template('index.html')

	script_file = os.path.basename(sequence + '.dc')
	if ' ' in script_file or 'flag' in script_file:
		return ':('

	proc = subprocess.run(
		['dc', script_file], 
		capture_output=True,
		text=True,
		timeout=1,
	)
	output = proc.stdout

	return render_template('index.html', output=output)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080)
