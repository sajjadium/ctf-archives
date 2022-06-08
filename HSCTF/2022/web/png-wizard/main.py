#!/usr/bin/env python3
import itertools
import os
import subprocess
import sys
from pathlib import Path

import flask
from flask import Flask, abort, redirect, render_template, request
from flask.helpers import url_for
from flask.wrappers import Response

UPLOAD_FOLDER = '/upload'

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB

def rand_name():
	return os.urandom(16).hex()

def is_valid_extension(filename: Path):
	return (
		filename.suffix.lower().lstrip(".")
		in ("gif", "jpg", "jpeg", "png", "tiff", "tif", "ico", "bmp", "ppm")
	)

@app.route("/", methods=["GET"])
def get():
	return render_template("index.html")

@app.route("/", methods=["POST"])
def post():
	if "file" not in request.files:
		return render_template("index.html", error="No file provided")
	file = request.files["file"]
	if not file.filename:
		return render_template("index.html", error="No file provided")
	if len(file.filename) > 64:
		return render_template("index.html", error="Filename too long")
	
	filename = Path(UPLOAD_FOLDER).joinpath("a").with_name(file.filename)
	if not is_valid_extension(filename):
		return render_template("index.html", error="Invalid extension")
	
	file.save(filename)
	
	new_name = filename.with_name(rand_name() + ".png")
	
	try:
		subprocess.run(
			f"convert '{filename}' '{new_name}'",
			shell=True,
			check=True,
			stderr=subprocess.PIPE,
			timeout=5,
			env={},
			executable="/usr/local/bin/shell"
		)
	except subprocess.TimeoutExpired:
		return render_template("index.html", error="Command timed out")
	except subprocess.CalledProcessError as e:
		return render_template(
			"index.html",
			error=f"Error converting file: {e.stderr.decode('utf-8',errors='ignore')}"
		)
	finally:
		filename.unlink()
	
	return redirect(url_for("converted_file", filename=new_name.name))

@app.route('/converted/<filename>')
def converted_file(filename):
	path = Path(UPLOAD_FOLDER).joinpath("a").with_name(filename)
	if not path.exists():
		# imagemagick sometimes generates multiple images depending on the src image
		oldpath = path
		path = oldpath.with_name(f"{oldpath.stem}-0{oldpath.suffix}")
		if path.exists():
			for i in itertools.count(1):
				path2 = oldpath.with_name(f"{oldpath.stem}-{i}{oldpath.suffix}")
				if not path2.exists():
					break
				path2.unlink()
		else:
			abort(404)
	
	def generate():
		with path.open("rb") as f:
			yield from f
		path.unlink()
	
	return Response(generate(), mimetype="image/png")

@app.route("/version")
def version():
	python_version = sys.version
	flask_version = str(flask.__version__)
	magick_version = subprocess.run(
		"convert -version", shell=True, check=False, stdout=subprocess.PIPE
	).stdout.decode()
	
	return render_template(
		"version.html",
		python_version=python_version,
		flask_version=flask_version,
		magick_version=magick_version
	)

if __name__ == "__main__":
	app.run()
