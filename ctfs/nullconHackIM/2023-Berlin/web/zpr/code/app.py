from flask import Flask, Response, request
from werkzeug.utils import secure_filename
from subprocess import check_output
import io
import hashlib
import secrets
import zipfile
import os
import random
import glob

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1.5 * 1000 # 1kb

@app.route('/', methods=['GET'])
def index():
	output = io.StringIO()
	output.write("Send me your zipfile as a POST request and I'll make them accessible to you ;-0.")

	return Response(output.getvalue(), mimetype='text/plain')


@app.route('/', methods=['POST'])
def upload():
	output = io.StringIO()
	if 'file' not in request.files:
		output.write("No file provided!\n")
		return Response(output.getvalue(), mimetype='text/plain')

	try:
		file = request.files['file']

		filename = hashlib.md5(secrets.token_hex(8).encode()).hexdigest()
		dirname = hashlib.md5(filename.encode()).hexdigest()

		dpath = os.path.join("/tmp/data", dirname)
		fpath = os.path.join(dpath, filename + ".zip")

		os.mkdir(dpath)
		file.save(fpath)


		with zipfile.ZipFile(fpath) as zipf:
			files = zipf.infolist()
			if len(files) > 5:
				raise Exception("Too many files!")

			total_size = 0
			for the_file in files:
				if the_file.file_size > 50:
					raise Exception("File too big.")

				total_size += the_file.file_size

			if total_size > 250:
				raise Exception("Files too big in total")

		check_output(['unzip', '-q', fpath, '-d', dpath])


		g = glob.glob(dpath + "/*")
		for f in g:
			output.write("Found a file: " + f + "\n")

		output.write("Find your files at http://...:8088/" + dirname + "/\n")


	except Exception as e:
		output.write("Error :-/\n")

	return Response(output.getvalue(), mimetype='text/plain')



if __name__ == "__main__":
	app.run(host='0.0.0.0', port='8080', debug=True)