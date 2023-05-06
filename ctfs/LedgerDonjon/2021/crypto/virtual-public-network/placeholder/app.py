#!/usr/bin/env python3

from flask import Flask
import os

app = Flask(__name__)

#insert your challenge here, only accessible through the vpn !

@app.route("/", methods=['GET'])
def index():
    return "Hello World, the flag is %s" % os.environ.get("FLAG")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
