#!/usr/bin/env python3

from flask import Flask, render_template, request
import subprocess
import uuid
import os
from os import path
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def upload_file():
    return render_template('./upload.html')
    
@app.route('/stegsolver', methods = ['POST'])
def process_file():
    if request.method == 'POST':
        if 'file' in request.files and 'passphrase' in request.form:
            f = request.files['file']
            stegfile_name = str(uuid.uuid4())
            outfile_name = str(uuid.uuid4())
            f.save(app.config['UPLOAD_FOLDER'] + stegfile_name)
            os.chdir(app.config['UPLOAD_FOLDER'])
            try:
                subprocess.run(['steghide', 'extract', '-sf', stegfile_name, '-p', request.form['passphrase'], '-xf', outfile_name], check=True, timeout=60)
            except Exception:
                os.chdir('..')
                if path.exists(app.config['UPLOAD_FOLDER'] + stegfile_name):
                    os.remove(app.config['UPLOAD_FOLDER'] + stegfile_name)
                if path.exists(app.config['UPLOAD_FOLDER'] + outfile_name):
                    os.remove(app.config['UPLOAD_FOLDER'] + outfile_name)
                return 'Either no data was embedded, or something went wrong with the extraction'
            os.chdir("..")
            if path.exists(app.config['UPLOAD_FOLDER'] + outfile_name):
                outfile = open(app.config['UPLOAD_FOLDER'] + outfile_name, "rb")
                result = outfile.read()
                outfile.close()
                if path.exists(app.config['UPLOAD_FOLDER'] + stegfile_name):
                    os.remove(app.config['UPLOAD_FOLDER'] + stegfile_name)
                if path.exists(app.config['UPLOAD_FOLDER'] + outfile_name):
                    os.remove(app.config['UPLOAD_FOLDER'] + outfile_name)
                return result
            else:
                if path.exists(app.config['UPLOAD_FOLDER'] + stegfile_name):
                    os.remove(app.config['UPLOAD_FOLDER'] + stegfile_name) 
                return 'Either no data was embedded, or something went wrong with the extraction'
        else:
            return 'Either the passphrase or the file is missing.'
    else:
        return 'Invalid request type'

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000)
