from flask import Flask, request, render_template
from urllib.request import urlopen
from waitress import serve
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

app = Flask(
        __name__,
        static_url_path='/static',
        static_folder='./static',
        )

PREMIUM_TOKEN = os.urandom(32).hex()

limiter = Limiter(app, key_func=get_remote_address)

@app.after_request
def add_headers(response):
    response.cache_control.max_age = 120
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy/<path:path>')
@limiter.limit("10/minute")
def proxy(path):
    remote_addr = request.headers.get('X-Forwarded-For') or request.remote_addr
    is_authorized = request.headers.get('X-Premium-Token') == PREMIUM_TOKEN or remote_addr == "127.0.0.1"
    try:
        page = urlopen(path, timeout=.5)
    except:
        return render_template('proxy.html', auth=is_authorized)
    if is_authorized:
        output = page.read().decode('latin-1')
    else:
        output = f"<pre>{page.headers.as_string()}</pre>"
    return render_template('proxy.html', auth=is_authorized, content=output)

@app.route('/premium')
def premium():
    return "we're sorry, but premium membership is not yet available :( please check back soon!"

serve(app, host="0.0.0.0", port=3000, threads=20)
