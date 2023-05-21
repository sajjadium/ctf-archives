from flask import Flask, Response, jsonify
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", os.urandom(512).hex())
FLAG = os.environ.get("FLAG", "greyctf{fake_flag}")


@app.route("/")
def index() -> Response:
    """Main page of flag service"""
    # Users can't see this anyways so there is no need to beautify it
    # TODO Create html for the page
    return jsonify({"message": "Welcome to the homepage"})


@app.route("/flag")
def flag() -> Response:
    """Flag endpoint for the service"""
    return jsonify({"message": f"This is the flag: {FLAG}"})


@app.route("/construction")
def construction() -> Response:
    return jsonify({"message": "The webpage is still under construction"})
