from flask import Flask, Response, request, jsonify
from urllib.parse import unquote
import requests
import json
import os


app = Flask(__name__) 

appHost = 'http://'+os.environ['APP_HOSTNAME']+':10000/'

@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def catch_all(path):
    print(path, unquote(path))
    
    if('gettoken' in unquote(path)):
        promo = request.args.get('promocode')
        creditcard = request.args.get('creditcard')

        if promo == 'FREEWAF':
            res = jsonify({'err':'Sorry, this promo has expired'})
            res.status_code = 400
            return res

        r = requests.get(appHost+path, params={'promocode':promo,'creditcard':creditcard})

    else:
        r = requests.get(appHost+path)
    
    headers = [(name, value) for (name, value) in r.raw.headers.items()]
    res = Response(r.content, r.status_code, headers)
    return res

@app.route('/search', methods=['POST'])
def search():
    j = request.get_json(force=True)
    
    badReq = False
    if 'name' in j:
        x = j['name']
        if not isinstance(x, str) or not x.isalnum():
            badReq = True
    if 'min_radius' in j:
        x = j['min_radius']
        if not isinstance(x, int):
            badReq = True
    if 'max_radius' in j:
        x = j['max_radius']
        if not isinstance(x, int):
            badReq = True

    if badReq:
        res = jsonify({'err':'Bad request, filtered'})
        res.status_code = 400
        return res

    token = name = request.cookies.get('token')
    r = requests.post(appHost+'search',data=request.data,cookies={'token':token})

    headers = [(name, value) for (name, value) in r.raw.headers.items()]

    res = Response(r.content, r.status_code, headers)
    return res

def create_app(): 
    return app