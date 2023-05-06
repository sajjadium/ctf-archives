from flask import Flask, render_template, request
import html
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

blacklist = ["flag", "cat", "|", "&", ";", "`", "$"]

@app.route('/backend')
def backend():
    for word in blacklist:
        if word in request.args['query']:
            return "Stop hacking.\n"
    return html.escape(os.popen(f"sed {request.args['query']} stuff.txt").read())
