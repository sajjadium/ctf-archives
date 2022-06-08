import os
from flask import Flask, session, render_template, request, redirect

app = Flask(__name__)
app.secret_key = os.environ["SECRET"]

@app.route("/create")
def create():
	return render_template("create.html")

@app.route("/")
def index():
	return redirect("/create")

@app.route("/display")
def display():
	return render_template("display.html")

@app.route("/login", methods=["POST"])
def login():
	if "username" in request.form:
		session["username"] = request.form["username"]
		return redirect(request.referrer or "/")
	else:
		return "Username not provided", 400

@app.route("/help")
def help():
	return render_template("help.html")

if __name__ == "__main__":
	app.run()
