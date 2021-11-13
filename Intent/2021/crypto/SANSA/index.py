import os
from flask import Flask, request, render_template
from verify_file import verify_data
import base64
from logging import *
import yaml
import json

app = Flask(__name__, template_folder=".", static_folder="public", static_url_path="/")
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(32))


@app.route('/')
def index():
    return render_template('index.html')


@app.post("/sansa_update")
def verify_update():
    try:
        data = json.loads(request.files['file'].read())
    except:
        return "invalid json file"

    try:
        update_content = base64.b64decode(bytes(data["content"], 'utf-8'))
        update_signature = data["signature"]
    except:
        return "invalid SANSA structure"

    if verify_data(update_content, update_signature):
        return "<HERE_GOES_THE_FLAG>"
    else:
        return "invalid signature"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)