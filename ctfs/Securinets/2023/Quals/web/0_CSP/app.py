import os
import re
from flask import Flask, request, jsonify, escape
import random
import string

import requests

app = Flask(__name__)
url = os.environ.get("URL_BOT")

user_tokens = {}
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': ' *',
    'Access-Control-Max-Age': '3600',
}


def use_regex(input_text):
    pattern = re.compile(r"https://escape.nzeros.me/", re.IGNORECASE)
    return pattern.match(input_text)


def generate_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=12))




@app.route('/reporturl', methods=['POST', 'OPTIONS'])
def report():
    if request.method == "OPTIONS":
        return '', 200, headers
    if request.method == "POST":
        link = request.form['link']
        if not use_regex(link):
            return "wrong url format", 200, headers

        obj = {'url': link}
        # send to bot
        x = requests.post(url, json=obj)
        if (x.content == b'OK'):
            return "success!", 200, headers

    return "failed to visit", 200, headers


@app.route('/GetToken', methods=['GET', 'OPTIONS'])
def get_token():

    if request.method == "OPTIONS":
        return '', 200, headers

    try:
        new_header: dict[str, str | bytes] = dict(headers)
        userid = request.args.get("userid")

        if not userid:
            return jsonify({'error': 'Missing userid'}), 400, headers

        if userid in user_tokens:
            token = user_tokens[userid]
        else:
            token = generate_token()
            user_tokens[userid] = token
        new_header["Auth-Token-" +
                   userid] = token

        return jsonify({'token': token, 'user': str(escape(userid))[:110]}), 200, new_header

    except Exception as e:
        return jsonify({'error': f'Something went wrong {e}'}), 500, headers


@app.route('/securinets', methods=['GET', 'OPTIONS'])
def securinets():

    if request.method == "OPTIONS":
        return "", 200, headers
    token = None
    for key, value in request.headers.items():
        if 'Auth-Token-' in key:
            token_name = key[len('Auth-Token-'):]
            token = request.headers.get('Auth-Token-'+token_name)

    if not token:
        return jsonify({'error': 'Missing Auth-Token header', }), 401, headers

    if token in user_tokens.values():
        return jsonify({'message': f'Welcome to Securinets. {token_name}'}), 200, headers
    else:
        return jsonify({'error': 'Invalid token or user not found'}), 403, headers


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000", debug=False)
