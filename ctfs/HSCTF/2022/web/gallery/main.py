import os
import re
from pathlib import Path
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
IMAGE_FOLDER = Path("/images")

@app.route("/")
def index():
	images = [p.name for p in IMAGE_FOLDER.iterdir()]
	return render_template("index.html", images=images)

@app.route("/image")
def image():
	if "image" not in request.args:
		return "Image not provided", 400
	if ".jpg" not in request.args["image"]:
		return "Invalid filename", 400
	
	file = IMAGE_FOLDER.joinpath(Path(request.args["image"]))
	if not file.is_relative_to(IMAGE_FOLDER):
		return "Invalid filename", 400
	
	try:
		return send_file(file.resolve())
	except FileNotFoundError:
		return "File does not exist", 400

@app.route("/flag")
def flag():
	if 2 + 2 == 5:
		return send_file("/flag.txt")
	else:
		return "No.", 400

if __name__ == "__main__":
	app.run()
