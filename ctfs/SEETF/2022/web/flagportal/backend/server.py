from waitress import serve
from flask import Flask, request

import os, requests

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/flag-count')
def flag_count():
    return '2'

@app.route('/flag-plz', methods=['POST'])
def flag():
    if request.headers.get('ADMIN_KEY') == os.environ['ADMIN_KEY']:
        if 'target' not in request.form:
            return 'Missing URL'

        requests.post(request.form['target'], data={
            'flag': os.environ['SECOND_FLAG'],
            'congrats': 'Thanks for playing!'
        })

        return 'OK, flag has been securely sent!'
            
    else:
        return 'Access denied'

@app.route('/forbidden')
def forbidden():
    return 'Forbidden', 403

serve(app, host='0.0.0.0', port=80)