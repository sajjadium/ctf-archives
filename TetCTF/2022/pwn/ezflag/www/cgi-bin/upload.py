#!/usr/bin/env python3

import os
import cgi
import base64
import socket

def write_header(key, value) -> None:
    print('{:s}: {:s}'.format(key, value))

def write_status(code, msg) -> None:
    print('Status: {:d} {:s}'.format(code, msg), end='\n\n')

def write_location(url) -> None:
    print('Location: {:s}'.format(url), end='\n\n')

def handle_get() -> None:
    with open('../html/upload.html', 'rb') as f:
        dat = f.read()

    write_header('Content-Type', 'text/html')
    write_header('Content-Length', str(len(dat)))
    write_status(200, 'OK')
    print(dat.decode('utf-8'), end=None)

def valid_file_name(name) -> bool:
    if len(name) == 0 or name[0] == '/':
        return False
    if '..' in name:
        return False
    if '.py' in name:
        return False
    return True

def handle_post() -> None:
    fs = cgi.FieldStorage()
    item = fs['file']
    if not item.file:
        write_status(400, 'Bad Request')
        return
    if not valid_file_name(item.filename):
        write_status(400, 'Bad Request')
        return
    normalized_name = item.filename.strip().replace('./', '')
    path = ''.join(normalized_name.split('/')[:-1])
    os.makedirs('../upload/' + path, exist_ok=True)
    with open('../upload/' + normalized_name, 'wb') as f:
        f.write(item.file.read())
    write_location('/uploads/' + normalized_name)

def check_auth() -> bool:
    auth = os.environ.get('HTTP_AUTHORIZATION')
    if auth is None or len(auth) < 6 or auth[0:6] != 'Basic ':
        return False
    auth = auth[6:]
    try:
        data = base64.b64decode(auth.strip().encode('ascii')).split(b':')
        if len(data) != 2:
            return False
        username = data[0]
        password = data[1]
        if len(username) > 8 or len(password) > 16:
            return False
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', 4444))
        s.settimeout(5)
        s.send(username + b'\n' + password + b'\n')
        result = s.recv(1)
        s.close()
        if result == b'Y':
            return True
        return False
    except:
        return False

if __name__ == '__main__':
    if not check_auth():
        write_header('WWW-Authenticate', 'Basic')
        write_status(401, 'Unauthorized')
    else:
        method = os.environ.get('REQUEST_METHOD')
        if method == 'POST':
            handle_post()
        elif method == 'GET':
            handle_get()
        else:
            write_status(405, 'Method Not Allowed')
