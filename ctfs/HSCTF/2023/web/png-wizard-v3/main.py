#!/usr/bin/env python3
import os
import sys
from pathlib import Path

import pi_heif
from flask import Flask, abort, redirect, render_template, request
from flask.helpers import url_for
from flask.wrappers import Response
from PIL import Image
from svglib.svglib import SvgRenderer
from reportlab.graphics import renderPM
from lxml import etree

UPLOAD_FOLDER = '/upload'

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB

with open("requirements.txt", encoding="utf-8") as reqs:
	requirements_version = reqs.read()

# smh why doesn't Pillow have native support for this
pi_heif.register_heif_opener()

def rand_name():
	return os.urandom(16).hex()

def is_valid_extension(filename: Path):
	return (
		filename.suffix.lower().lstrip(".") in (
		"gif", "jpg", "jpeg", "png", "tiff", "tif", "ico", "bmp", "ppm", "webp", "svg", "heic",
		"heif"
		)
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
	
	filename = Path(UPLOAD_FOLDER).joinpath("a").with_name(rand_name() + Path(file.filename).suffix)
	if not is_valid_extension(filename):
		return render_template("index.html", error="Invalid extension")
	
	file.save(filename)
	
	new_name = filename.with_name(rand_name() + ".png")
	
	try:
		# smh why doesn't Pillow have native support for this
		if filename.suffix.lower() == ".svg":
			svg_root = etree.parse(filename, parser=etree.XMLParser()).getroot()
			drawing = SvgRenderer(filename).render(svg_root)
			renderPM.drawToFile(drawing, new_name, fmt=".PNG")
		else:
			with Image.open(
				filename,
				formats=["GIF", "JPEG", "PNG", "TIFF", "ICO", "BMP", "WEBP", "HEIF", "PPM"]
			) as img:
				img.save(new_name)
	except Exception as e:
		return render_template("index.html", error=f"Error converting file: {str(e)}")
	finally:
		filename.unlink()
	
	return redirect(url_for("converted_file", filename=new_name.name))

@app.route('/converted/<filename>')
def converted_file(filename):
	path = Path(UPLOAD_FOLDER).joinpath("a").with_name(filename)
	if not path.exists():
		abort(404)
	
	def generate():
		try:
			with path.open("rb") as f:
				yield from f
		finally:
			path.unlink()
	
	return Response(generate(), mimetype="image/png")

@app.route("/version")
def version():
	python_version = sys.version
	
	return render_template(
		"version.html",
		python_version=python_version,
		requirements_version=requirements_version,
	)

if __name__ == "__main__":
	app.run()
