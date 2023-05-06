#!/usr/local/bin/python3 -u
from gevent import monkey
monkey.patch_all()

import json
import os
from gevent.pywsgi import WSGIServer
from flask import Flask, Response, request
from prometheus_client import Summary, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware


app = Flask(__name__)

ORACLE_TIME = Summary('oracle_processing_seconds', 'Time spent processing oracle request')
FLAG_TIME = Summary('flag_processing_seconds', 'Time spent processing flag request')


with open('secret.json') as f:
    FLAG, s, p = json.load(f)
    s, p = int(s), int(p)
    assert 0 < s < 2**100
    assert 0 < p < 2**1025


@app.route('/oracle', methods=['GET'])
@ORACLE_TIME.time()
def oracle():
    try:
        x = int(request.args['x']) % p
    except Exception:
        return Response("(._.)???", mimetype="text/plain; charset=utf8")
    return Response(str(pow(x, s, p)), mimetype="text/plain; charset=utf8")


@app.route('/flag', methods=['GET'])
@FLAG_TIME.time()
def flag():
    try:
        x = int(request.args['x']) % p
    except Exception:
        return Response("(._.)???", mimetype="text/plain; charset=utf8")
    if pow(x, s, p) == 1337:
        return Response(FLAG, mimetype="text/plain; charset=utf8")
    else:
        return Response("{>_<}!!!", mimetype="text/plain; charset=utf8")


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, { '/metrics': make_wsgi_app() })
if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 27492), app).serve_forever()
