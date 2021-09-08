import asyncio
import hashlib
import hmac
import time
import uuid
import re
import binascii
import base64
import socket
from urllib.parse import unquote
from datetime import datetime
from logzero import logger
from functools import wraps
import sqlite3
import requests
from threading import Thread
from flask import Flask, make_response, render_template, g, url_for, request, Response, copy_current_request_context, jsonify

# run the server: python -m flask run --host=0.0.0.0 --port=1024

try:
    SECRET = open('/tmp/secret', 'rb').read()
except FileNotFoundError:
    SECRET = uuid.uuid4().bytes
    with open('/tmp/secret', 'wb') as f:
        f.write(SECRET)

try:
    BACKEND = socket.getaddrinfo('app', 0)[0][4][0]
except socket.gaierror:
    BACKEND = '127.0.0.1'

BACKEND_URL = f'http://{BACKEND}:5000/'

app = Flask(__name__)

# the WAF is still early in development and only protects a few cases
def waf_param(param):
    MALICIOUS = ['select', 'union', 'alert', 'script', 'sleep', '"', '\'', '<']
    for key in param:
        val = param.get(key, '')
        while val != unquote(val):
            val = unquote(val)

        for evil in MALICIOUS:
            if evil.lower() in val.lower():
                raise Exception('hacker detected')

from Crypto.Cipher import AES
#from Crypto.Random import get_random_bytes


def decrypt(val):
    encrypted = base64.b64decode(val[8:].encode())
    b64_nonce, b64_ciphertext, b64_tag = encrypted.split(b':')
    nonce = base64.b64decode(b64_nonce)
    ciphertext = base64.b64decode(b64_ciphertext)
    tag = base64.b64decode(b64_tag)
    cipher = AES.new(SECRET, AES.MODE_EAX, nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data

def encrypt(val):
    cipher = AES.new(SECRET, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(val.encode())
    encrypted = f'{base64.b64encode(cipher.nonce).decode()}:{base64.b64encode(ciphertext).decode()}:{base64.b64encode(tag).decode()}'

    b64 = base64.b64encode(encrypted.encode()).decode()
    return f'ENCRYPT:{b64}'

def encrypt_params(param):
    # We don't want to encrypt identifiers.
    # This is a default set of typical ID values.
    # In the future should be configurable per customer.
    IGNORE = ['uuid', 'id', 'pk', 'username', 'password']
    encrypted_param = {}
    for key in param:
        val = param.get(key,'')
        if key in IGNORE:
            encrypted_param[key] = val
        else:
            encrypted_param[key] = encrypt(val)
    
    return encrypted_param


def decrypt_data(data):
    cryptz = re.findall(r'ENCRYPT:[A-Za-z0-9+/]+=*', data.decode())
    for crypt in cryptz:
        try:
            data = data.replace(crypt.encode(), decrypt(crypt))
        except binascii.Error:
            data = data.replace(crypt.encode(), b'MALFORMED ENCRYPT')

            
    return data

def inject_ad(data):
    AD = b"""
        <div class="opacity-90 shadow-md w-full md:w-1/2 m-auto mt-10 mb-10 bg-yellow-300 px-5 py-5 rounded rounded-xl flex flex-row ">
            <div class="ml-5">
                <i class="text-white text-4xl fas fa-user-shield"></i>
            </div>
            <div class="flex-grow ml-5 text-center">
                User data is military encrypted by <span class="font-bold">AmazingCryptoWAF</span>&trade; <br>
            </div>
        </div>
    </body>"""
    return data.replace(b'</body>', AD)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET'])
def proxy(path):

    # Web Application Firewall
    try:
        waf_param(request.args)
        waf_param(request.form)
    except:
        return 'error'

    # contact backend server
    proxy_request = None
    query = request.query_string.decode()
    headers = {'Cookie': request.headers.get('Cookie', None) }
    if request.method=='GET':
        proxy_request = requests.get(f'{BACKEND_URL}{path}?{query}',
                            headers=headers,
                            allow_redirects=False)
    elif request.method=='POST':
        headers['Content-type'] = request.content_type
        proxy_request = requests.post(f'{BACKEND_URL}{path}?{query}', 
                            data=encrypt_params(request.form),
                            headers=headers,
                            allow_redirects=False)
    
    if not proxy_request:
        return 'error'

    
    response_data = decrypt_data(proxy_request.content)
    injected_data = inject_ad(response_data)
    resp = make_response(injected_data)
    resp.status = proxy_request.status_code
    if proxy_request.headers.get('Location', None):
        resp.headers['Location'] = proxy_request.headers.get('Location')
    if proxy_request.headers.get('Set-Cookie', None):
        resp.headers['Set-Cookie'] = proxy_request.headers.get('Set-Cookie')
    if proxy_request.headers.get('Content-Type', None):
        resp.content_type = proxy_request.headers.get('Content-Type')

    return resp
