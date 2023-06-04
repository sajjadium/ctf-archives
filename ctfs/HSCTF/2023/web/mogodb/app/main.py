import os
import traceback

import pymongo.errors
from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import MongoClient

app = Flask(__name__)
FLAG = os.getenv("FLAG")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024
mongo_client = MongoClient(connect=False)
db = mongo_client.database

@app.route("/", methods=["GET"])
def main():
	if "user" in session:
		return redirect(url_for("home"))
	if "error" in request.args:
		return render_template("login.html", error=request.args["error"])
	return render_template("login.html")

@app.route("/", methods=["POST"])
def login():
	if "user" not in request.form:
		return redirect(url_for("main", error="user not provided"))
	if "password" not in request.form:
		return redirect(url_for("main", error="password not provided"))
	
	try:
		user = db.users.find_one(
			{
			"$where":
				f"this.user === '{request.form['user']}' && this.password === '{request.form['password']}'"
			}
		)
	except pymongo.errors.PyMongoError:
		traceback.print_exc()
		return redirect(url_for("main", error="database error"))
	
	if user is None:
		return redirect(url_for("main", error="invalid credentials"))
	
	session["user"] = user["user"]
	session["admin"] = user["admin"]
	return redirect(url_for("home"))

@app.route("/register")
def register_get():
	if "error" in request.args:
		return render_template("register.html", error=request.args["error"])
	return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
	if "user" not in request.form:
		return redirect(url_for("register_get", error="user not provided"))
	if "password" not in request.form:
		return redirect(url_for("register_get", error="password not provided"))
	
	try:
		if db.users.find_one({"user": request.form["user"]}) is not None:
			return redirect(url_for("register_get", error="user already exists"))
		
		db.users.insert_one(
			{
			"user": request.form["user"],
			"password": request.form["password"],
			"admin": False
			}
		)
	except pymongo.errors.PyMongoError:
		traceback.print_exc()
		return redirect(url_for("register_get", error="database error"))
	
	session["user"] = request.form["user"]
	return redirect(url_for("main"))

@app.route("/home")
def home():
	if "user" not in session:
		return redirect(url_for("main", error="not logged in"))
	
	if "error" in request.args:
		return render_template("home.html", error=request.args["error"])
	
	return render_template("home.html", flag=FLAG)

@app.route("/logout")
def logout():
	session.pop("admin", None)
	session.pop("user", None)
	return redirect(url_for("main"))

if __name__ == "__main__":
	app.run()
