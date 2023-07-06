#!/usr/bin/env python3
from flask import Flask, request
import threading
import subprocess
import re

app = Flask(__name__)
FLAG = open('flag.txt').read()
lock = threading.Lock()

@app.route('/')
def index():
    return app.send_static_file('index.html')

key_to_check = "00000-00000-00000-00000-00000"
key_format = re.compile(r'^[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}-[0-9A-Z]{5}$')
@app.route('/check', methods=['GET', 'POST'])
def check():
    global key_to_check
    if request.method == 'GET':
        if request.remote_addr != '127.0.0.1':
            return "Forbidden", 403
        try:
            lock.release()
        except:
            pass
        return key_to_check
    else:
        key = request.form['key']
        if not key_format.match(key):
            return "Invalid key format", 400
        lock.acquire()
        key_to_check = key
        process = subprocess.Popen(['./node_modules/@devicescript/cli/devicescript', 'run', '-t', 'keychecker.devs'], stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            if b"success!" in line:
                process.terminate()
                return FLAG
        process.wait()
        return "Incorrect key", 400

