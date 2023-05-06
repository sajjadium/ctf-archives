#!/usr/bin/env python
# -*- coding:utf-8 -
from flask import Flask, request, redirect
from flask_session import Session
from io import BytesIO
import memcache
import pycurl
import random
import string

app = Flask(__name__)
app.debug = True
app.secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(56))

app.config['SESSION_TYPE'] = 'memcached'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = False
app.config['SESSION_KEY_PREFIX'] = 'actfSession:'
app.config['SESSION_MEMCACHED'] = memcache.Client(['127.0.0.1:11200'])

Session(app)

@app.route('/')
def index():
    buffer=BytesIO()
    if request.args.get('url'):
        url = request.args.get('url')
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.FTP_SKIP_PASV_IP, 0)
        c.setopt(c.WRITEDATA, buffer)
        blacklist = [c.PROTO_DICT, c.PROTO_FILE, c.PROTO_FTP, c.PROTO_GOPHER, c.PROTO_HTTPS, c.PROTO_IMAP, c.PROTO_IMAPS, c.PROTO_LDAP, c.PROTO_LDAPS, c.PROTO_POP3, c.PROTO_POP3S, c.PROTO_RTMP, c.PROTO_RTSP, c.PROTO_SCP, c.PROTO_SFTP, c.PROTO_SMB, c.PROTO_SMBS, c.PROTO_SMTP, c.PROTO_SMTPS, c.PROTO_TELNET, c.PROTO_TFTP]
        allowProtos = c.PROTO_ALL
        for proto in blacklist:
            allowProtos = allowProtos&~(proto)
        c.setopt(c.PROTOCOLS, allowProtos)
        c.perform()
        c.close()
        return buffer.getvalue().decode('utf-8')
    else:
        return redirect('?url=http://www.baidu.com',code=301)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)