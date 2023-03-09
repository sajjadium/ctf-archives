from flask import Flask, Response, request
import requests
import io

app = Flask(__name__)


@app.route('/')
def index():
	s = requests.Session()
	cookies = {'role': 'guest'}

	output = io.StringIO()
	output.write("Usage: Look at the code ;-)\n\n")
	try:
		output.write("Overwriting cookies with default value! This must be secure!\n")
		cookies = {**dict(request.cookies), **cookies}
		headers = {**dict(request.headers)}

		if cookies['role'] != 'guest':
			raise Exception("Illegal access!")

		r = requests.Request("GET", "http://backend:8080/whoami", cookies=cookies, headers=headers)
		prep = r.prepare()

		output.write("Prepared request cookies are: ")
		output.write(str(prep._cookies.items()))
		output.write("\n")
		output.write("Sending request...")
		output.write("\n")
		
		resp = s.send(prep, timeout=2.0)
		
		output.write("Request cookies are: ")
		output.write(str(resp.request._cookies.items()))
		output.write("\n\n")
		if 'Admin' in resp.content.decode():
			output.write("Someone's drunk oO\n\n")
		output.write("Response is: ")
		output.write(resp.content.decode())
		output.write("\n\n")
	except Exception as e:
		print(e)
		output.write("Error :-/" + str(e))
		output.write("\n\n")

	return Response(output.getvalue(), mimetype='text/plain')


if __name__ == "__main__":
	app.run(host='0.0.0.0', port='8080', debug=False)