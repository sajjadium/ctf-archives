import os
import traceback

import pymongo.errors
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient

app = Flask(__name__)
FLAG = os.getenv("FLAG")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET")
mongo_client = MongoClient(connect=False)
db = mongo_client.database

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/api/search", methods=["POST"])
def search():
	if request.json is None or "search" not in request.json:
		return jsonify({"error": "No search provided", "results": []}), 400
	try:
		results = db.flags.find(
			{
			"$where": f"this.challenge.includes('{request.json['search']}')"
			}, {
			"_id": False,
			"flag": False
			}
		).sort("challenge")
	except pymongo.errors.PyMongoError:
		traceback.print_exc()
		return jsonify({"error": "Database error", "results": []}), 500
	return jsonify({"error": "", "results": list(results)}), 200

if __name__ == "__main__":
	app.run()