import os
import traceback
import json
from flask import Flask, redirect, render_template, request, session, url_for, jsonify
import mariadb

app = Flask(__name__)
FLAG = os.getenv("FLAG")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024

conn = mariadb.connect(
	user="ctf", password=os.getenv("DB_PASSWORD"), host="localhost", database="ctf"
)

cursor = conn.cursor()

@app.route("/", methods=["GET"])
def main():
	if "user" in session:
		return redirect(url_for("home"))
	if "error" in request.args:
		return render_template("login.html", error=request.args["error"])
	return render_template("login.html")

@app.route("/api/login", methods=["POST"])
def login():
	raw_data = request.get_data()
	data = json.loads(raw_data)
	
	if "user" not in data:
		return jsonify({"error": "user not provided"}), 401
	if "password" not in data:
		return jsonify({"error": "password not provided"}), 401
	
	try:
		cursor.execute(
			"SELECT JSON_VALUE(data,'$.user'), CAST(JSON_VALUE(data, '$.admin') AS UNSIGNED) FROM users "
			"WHERE JSON_VALUE(data,'$.user') = ? AND JSON_VALUE(data, '$.password') = ?;",
			(data["user"], data["password"])
		)
		
		row = cursor.fetchone()
	except Exception:
		traceback.print_exc()
		return jsonify({"error": "database error"}), 500
	
	if row is None:
		return jsonify({"error": "invalid credentials"}), 400
	
	user, admin = row
	session["user"] = user
	session["admin"] = admin
	return jsonify({}), 200

@app.route("/register")
def register_get():
	if "error" in request.args:
		return render_template("register.html", error=request.args["error"])
	return render_template("register.html")

@app.route("/api/register", methods=["POST"])
def register():
	raw_data = request.get_data()
	data = json.loads(raw_data)
	
	if "user" not in data:
		return jsonify({"error": "user not provided"}), 401
	if "password" not in data:
		return jsonify({"error": "password not provided"}), 401
	
	if "admin" not in data or data["admin"]:
		return jsonify({"error": "invalid admin"}), 400
	
	try:
		cursor.execute(
			"SELECT data FROM users WHERE JSON_VALUE(data,'$.user') = ?;", (data["user"], )
		)
		if cursor.fetchone() is not None:
			return jsonify({"error": "user already exists"}), 400
		
		cursor.execute("INSERT INTO users (data) VALUES (?);", (raw_data, ))
	except Exception:
		traceback.print_exc()
		return jsonify({"error": "database error"}), 500
	
	session["user"] = data["user"]
	return jsonify({"error": ""}), 200

@app.route("/home")
def home():
	if "user" not in session:
		return redirect(url_for("main", error="not logged in"))
	
	return render_template("home.html", flag=FLAG)

@app.route("/logout")
def logout():
	session.pop("admin", None)
	session.pop("user", None)
	return redirect(url_for("main"))

if __name__ == "__main__":
	app.run()
