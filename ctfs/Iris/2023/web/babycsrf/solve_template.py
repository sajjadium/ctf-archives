from flask import Flask, request
import time

app = Flask(__name__)

with open("solve.html") as f:
    SOLVE = f.read()

@app.route("/")
def home():
    return SOLVE

# You can define functions that return non-static data too, of course
@app.route("/time")
def page():
    return f"{time.time()}"

# Run "ngrok http 12345"
# and submit the resulting https:// url to the admin bot
app.run(port=12345)
