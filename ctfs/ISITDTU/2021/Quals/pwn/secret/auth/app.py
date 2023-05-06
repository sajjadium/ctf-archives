#!/usr/bin/env python3

import base64
import binascii
import os
import hashlib
import socket
from Crypto.Util.number import long_to_bytes, bytes_to_long
from flask import Flask, session, request

app = Flask(__name__)
app.secret_key = 'VerySecretSecretKey'

N =  '''00:c7:cc:f7:ce:7c:15:63:d5:84:c1:eb:18:a4:08:
        63:b6:6f:dd:f7:ba:62:9f:02:82:1f:ce:a2:c9:25:
        c1:6b:ca:30:29:8e:67:6b:5c:8c:f5:a5:5e:b0:55:
        96:92:ea:dd:4d:1f:e1:c0:0c:6b:7a:68:33:49:f9:
        cc:60:6c:36:2d:92:46:20:5e:b0:e7:29:11:4c:25:
        6c:a3:d9:f8:07:60:36:2f:22:fa:3b:b4:96:d8:3d:
        99:58:35:50:49:bd:de:31:9e:81:52:35:5a:bc:6b:
        f4:c2:a2:69:a1:09:bf:46:9c:5a:47:33:f4:e0:5f:
        37:50:55:fd:80:b9:d7:96:2b'''

N = int(''.join(N.split()).replace(':', ''), 16)

def H(*args) -> bytes:
    m = hashlib.sha256()
    m.update(b''.join(long_to_bytes(x) for x in args))
    return bytes_to_long(m.digest()) % N

g = 2
k = H(N, g)
s = bytes_to_long(os.urandom(64))
I = b'admin'
p = binascii.hexlify(os.urandom(64))
v = pow(g, H(s, H(bytes_to_long(I + b':' + p))), N)
socks = {}

@app.route('/pre_auth', methods=['POST'])
def pre_auth():
    if 'auth' in session:
        return b'', 400
    j = request.get_json(force=True)
    if j['I'] != I.decode('ascii'):
        return b'', 403
    session['A'] = int(j['A'], 16)
    b = bytes_to_long(os.urandom(64))
    session['B'] = (k * v + pow(g, b, N)) % N
    u = H(session['A'], session['B'])
    S = pow(session['A'] * pow(v, u, N), b, N)
    session['K'] = H(S)
    resp = {
        's': hex(s),
        'B': hex(session['B'])
    }
    return resp, 200

@app.route('/auth', methods=['POST'])
def auth():
    if 'auth' in session:
        return b'', 400
    if 'K' not in session:
        return b'', 403
    j = request.get_json(force=True)
    M = int(j['M'], 16)
    MM = H(H(N) ^ H(g), H(bytes_to_long(I)), s, session['A'], session['B'], session['K'])
    if M != MM:
        return b'', 403
    resp = {
        'M': hex(H(session['A'], M, session['K']))
    }
    session.clear()
    session['auth'] = binascii.hexlify(os.urandom(8))
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.connect(('backend', 31337))
    socks[session['auth']] = ss
    return resp, 200

@app.route('/secret', methods=['POST'])
def secret():
    if 'auth' not in session:
        return b'', 403

    ss = socks[session['auth']]
    j = request.get_json(force=True)

    cmd = base64.b64decode(j['cmd'])
    if len(cmd) > 8:
        return b'', 400
    if len(cmd) < 8:
        cmd += b'\n'

    try:
        ss.sendall(cmd)
    except:
        del socks[session['auth']]
        session.clear()
        return b'', 500

    if cmd[0] == ord(b'0'):
        data = base64.b64decode(j['data'])
        if len(data) > 0x400:
            return b'', 400
        if len(data) < 0x400:
            data += b'\n'

        try:
            ss.sendall(data)
        except:
            del socks[session['auth']]
            session.clear()
            return b'', 500

    try:
        l = ss.recv(1)[0]
        data = b''
        while len(data) < l:
            data += ss.recv(l - len(data))
        return {
            'data': base64.b64encode(data).decode('ascii')
        }, 200
    except:
        del socks[session['auth']]
        session.clear()
        return b'', 500
