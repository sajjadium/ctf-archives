#!/usr/bin/env python3

from octothorpe import octothorpe

from base64 import b64decode, b64encode
from datetime import datetime, timedelta, timezone
from flask import Flask, make_response, redirect, render_template, request
from socket import MSG_WAITALL, socket
from struct import unpack
from urllib.parse import parse_qsl, unquote_to_bytes

app = Flask(__name__)
with open('/server-secret', 'rb') as secret_file:
    secret = secret_file.read()
executor = ('127.0.1.1', 1024)

def verify(data, signature):
    if signature != octothorpe(secret + data).hexdigest():
        raise ValueError('Invalid signature')

def sign(data):
    return octothorpe(secret + data).hexdigest()

def parse(query_string):
    return dict(parse_qsl(query_string, errors='ignore')), unquote_to_bytes(query_string)

@app.route('/api/authorize', methods=['GET'])
def authorize():
    args, decoded = parse(request.query_string)
    command = args.get(b'cmd')
    if not command:
        return {'error': 'No command specified'}, 400
    if command != b'ls':
        return {'error': 'Insufficient privileges'}, 403
    expiry = int((datetime.now(timezone.utc) + timedelta(seconds=15)).timestamp())
    expiry_arg = b'expiry=' + str(expiry).encode() + b'&'
    response = make_response(redirect(b'/api/run?' + expiry_arg + request.query_string, code=307))
    response.set_cookie('signature', sign(expiry_arg + decoded), max_age=30)
    return response

@app.route('/api/run', methods=['GET'])
def run_command():
    args, decoded = parse(request.query_string)
    signature = request.cookies.get('signature')
    if not signature:
        return {'error': 'Missing token'}, 403
    try:
        verify(decoded, signature)
    except ValueError as error:
        return {'error': 'Invalid token', 'detail': str(error)}, 403
    command = args.get(b'cmd')
    expiry = float(args.get(b'expiry'))
    if datetime.now(timezone.utc).timestamp() >= expiry:
        return {'error': 'Token has expired'}, 403
    try:
        with socket() as so:
            so.settimeout(0.5)
            so.connect(executor)
            so.sendall(command + b'\n')
            status, out_len, err_len = unpack('III', so.recv(12, MSG_WAITALL))
            stdout = so.recv(out_len, MSG_WAITALL)
            stderr = so.recv(err_len, MSG_WAITALL)
        return {
            'status': status,
            'stdout': b64encode(stdout).decode(),
            'stderr': b64encode(stderr).decode()
        }, 200
    except:
        return {'error': 'Failed to execute command'}, 500
