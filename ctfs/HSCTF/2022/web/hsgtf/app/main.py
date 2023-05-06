import os
import re
from flask import Flask, render_template, request

app = Flask(__name__)
USER_FLAG = os.environ["USER_FLAG"]
ADMIN_FLAG = os.environ["FLAG"]
ADMIN_SECRET = os.environ["ADMIN_SECRET"]

@app.route("/guess")
def create():
	if "guess" not in request.args:
		return "No guess provided", 400
	guess = request.args["guess"]
	
	if "secret" in request.cookies and request.cookies["secret"] == ADMIN_SECRET:
		flag = ADMIN_FLAG
	else:
		flag = USER_FLAG
	
	correct = flag.startswith(guess)
	return render_template("guess.html", correct=correct, guess=guess)

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == "__main__":
	app.run()
