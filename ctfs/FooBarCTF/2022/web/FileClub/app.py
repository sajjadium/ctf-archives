#!/usr/bin/python3

from asyncio import subprocess
from flask import Flask, Response, redirect, request, render_template
from werkzeug.exceptions import RequestEntityTooLarge
from string import ascii_lowercase, digits
from random import choice
import os, tarfile, wave
from PIL import Image
import yaml
import zipfile

app = Flask(__name__)

UPLOAD_FOLDER = "./uploads/"
EXTRACT_FOLDER = "./extracted/"
charset = digits + ascii_lowercase

random_string = lambda: "".join(choice(charset) for _ in range(10))

def valid_png(file):
    try:
        img = Image.open(file)
        if(img.format == 'PNG'):
            pass
        return True
    except:
        return False
def valid_wave(file):
    try :
        with wave.open(file):
            pass
        return True
    except:
        return False

def valid_pdf(file):
    return_code = os.system(f"pdfinfo {file} >/dev/null 2>&1")
    return return_code == 0

def valid_zip(file):
    try :
        with zipfile.ZipFile(file):
           return True
    except:
          return False

def valid_tar(file):
    try :
        with tarfile.open(file):
            pass
        return True
    except:
        return False

def check(file):
    if valid_tar(file) and valid_wave(file) and valid_pdf(file) and not valid_png(file):
        try:
            with tarfile.open(file) as tar:
                tar.extractall(EXTRACT_FOLDER)
        except Exception as e:
            print(e)
            return False
        print("Files extracted")
        try:
            with open('{}test.yaml'.format(EXTRACT_FOLDER),'r') as stream:
                output = yaml.load(stream,Loader=yaml.FullLoader)     
        except Exception as e:
            print(e)
            os.system(f'rm -rf {EXTRACT_FOLDER}/*')
            return False
        os.system(f'rm -rf {EXTRACT_FOLDER}/*')
        isvalid = True
    else:
        isvalid = False
    os.system(f"rm {file}")
    return isvalid

@app.route("/", methods=["GET"])
def root():
    return render_template("index.html")
    
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == "POST":
        f = request.files.get('upload-file')
        if not f:
            return render_template("nofile.html"), 400
        file_location = os.path.join(UPLOAD_FOLDER, random_string())
        f.save(file_location)
        if check(file_location):
            return render_template("success.html")
        else:
            return render_template("fail.html")
    else:
        return redirect("/")
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404