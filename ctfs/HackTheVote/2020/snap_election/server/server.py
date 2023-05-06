#!/usr/bin/env python3

import os
import json
import tempfile
import subprocess

from flask import Flask, request, abort, jsonify, send_file 
from werkzeug.utils import secure_filename

DEVNULL = open(os.devnull,'w')

app = Flask(__name__)
# Set max file size
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024

# Create tmp dir to hold uploads
if not os.path.exists('tmp'):
    os.mkdir('tmp')

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/tally',methods=['GET', 'POST'])
def upload():
    if 'file' not in request.files:
        return jsonify(error="Missing CSV File") 

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="Missing CSV File") 

    # Copy file into a tmp dir
    tmpdir = tempfile.TemporaryDirectory(dir=os.path.join(os.getcwd(), 'tmp'))
    filename = secure_filename(file.filename)

    path = os.path.join(tmpdir.name, filename)
    file.save(path)

    # Run counter program
    ballot_path = os.path.join(os.getcwd(), 'ballot.json')
    p = subprocess.Popen(
        ['timeout','5','htv-vote-counter',ballot_path,filename],
        cwd=tmpdir.name,
        stderr=DEVNULL,
        stdout=subprocess.PIPE
    )

    # Validate json output
    try:
        res = json.loads(p.communicate()[0])
    except:
        return jsonify(error="Could not parse JSON output") 

    tmpdir.cleanup()
    return jsonify(res)







if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
