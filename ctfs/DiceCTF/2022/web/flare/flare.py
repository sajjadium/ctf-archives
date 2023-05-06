import os
import ipaddress

from flask import Flask, request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
flag = os.getenv('FLAG', default='dice{flag}')

@app.route('/')
def index():
    ip = ipaddress.ip_address(request.headers.get('CF-Connecting-IP'))

    if isinstance(ip, ipaddress.IPv4Address) and ip.is_private:
        return flag

    return f'No flag for {format(ip)}'

WSGIServer(('', 8080), app).serve_forever()