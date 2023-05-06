#!/usr/bin/env python3

import uuid
import os
import shutil
import tarfile
import time
import re

from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 4 * 1000 * 1000

@app.route("/")
def upload():
    return render_template('./upload.html')

@app.route('/uploader', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        old_umask = os.umask(0o77)
        dir_name = os.path.join('/tmp/tmp', str(uuid.uuid4()))
        file_name = os.path.join(dir_name, str(uuid.uuid4()))
        os.makedirs(dir_name, exist_ok=True)
        try:
            f = request.files['file']
            f.save(file_name)

            if tarfile.is_tarfile(file_name):
                mal = False
                with tarfile.open(file_name) as t:
                    for name in t.getnames():
                        if name[0] == '/' or '..' in name:
                            mal = True
                            break
                        mem = t.getmember(name)
                        if '/' in mem.linkname or '..' in mem.linkname:
                            mal = True
                            break
                    if not mal:
                        t.extractall(dir_name)
                os.remove(file_name)

                if not mal:
                    r = os.system('LD_PRELOAD=/home/want_my_signature/libmsgpackc.so.2 /home/want_my_signature/verify '+dir_name)
                    if r == 0:
                        ret = 'File uploaded successfully<br>Hi'
                    else:
                        ret = 'No hack! >:('
                else:
                    ret = 'No hack! >:('
            else:
                ret = 'Can only upload tar file >:('
        except Exception as e:
            ret = 'Something went wrong :( <br>' + str(e)
        finally:
            shutil.rmtree(dir_name)
            return ret
