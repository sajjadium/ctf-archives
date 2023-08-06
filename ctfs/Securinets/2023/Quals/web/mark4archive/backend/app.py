import json
import time
import os
from flask import Flask, render_template
from analyze import analyze_bp
from report import report_bp
from api import api_bp
from flask_sock import Sock


app = Flask(__name__)
app.register_blueprint(analyze_bp)
app.register_blueprint(report_bp)
app.register_blueprint(api_bp)
sock = Sock(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/instructions", methods=["GET"])
def instruction():
    return render_template("instruction.html")

@sock.route('/echo')
def echo(sock):
    total_size = 100
    progress = 0
    while progress < total_size:
        time.sleep(0.1)
        progress += 10
        sock.send(json.dumps({'progress': progress}))
    
    return "complete!"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
