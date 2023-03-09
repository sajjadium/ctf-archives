import os
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/whoami')
def whoami():
	role = request.cookies.get('role','guest')
	really = request.cookies.get('really', 'no')
	if role == 'admin':
		if really == 'yes':
			resp = 'Admin: ' + os.environ['FLAG']
		else:
			resp = 'Guest: Nope'
	else:
		resp = 'Guest: Nope'
	return Response(resp, mimetype='text/plain')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port='8080', debug=False)