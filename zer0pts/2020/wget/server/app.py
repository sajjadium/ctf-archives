#!/usr/bin/env python
from flask import Flask, request, render_template
import subprocess

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    url = None
    result = None
    
    if request.method == 'POST':
        if 'url' in request.form:
            url = request.form['url']
            result = omega_get(url)
    
    if url is None:
        url = "http://www.example.com/"
    
    return render_template('index.html', result=result, url=url)

def omega_get(url):
    if len(url) > 0x100:
        return "[ERROR] URL is too long"

    try:
        result = subprocess.check_output(
            ['/home/pwn/omega_get', url],
            stderr=subprocess.STDOUT,
            shell=True
        )
        return result.decode()
    except Exception as e:
        return '[ERROR] {}'.format(e)

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=9009)
