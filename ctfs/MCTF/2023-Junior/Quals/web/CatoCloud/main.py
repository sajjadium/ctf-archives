import os
import time
import requests
from string import ascii_lowercase
from itertools import product
from flask import *

ALPHABET = product(ascii_lowercase, repeat=3)

app = Flask(__name__)

import utils


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    global ALPHABET

    name = request.json.get('name')
    data = request.json.get('data')

    if not data or len(data) > 67108864 or not utils.verify_upload(name, data):
        return '#'

    next_id = ''.join(next(ALPHABET, []))

    if not next_id:
        ALPHABET = product(ascii_lowercase, repeat=3)
        utils.reset_storage()
        return '#'

    storage_size = sum(os.path.getsize(f'./storage/{file}') for file in os.listdir('./storage'))
    if storage_size + len(data) > 1073741824:  # 1 GB
        utils.reset_storage()
        return '#'

    if any((file.startswith(next_id) for file in os.listdir('./storage'))):
        return '#'

    with open(f'./storage/{next_id}_{name}', 'w', encoding='utf-8') as f:
        f.write(data)

    return next_id


@app.route('/<regex("[a-z]{3}/*"):address>')
def retrieve_file(address):
    target = requests.get(f'http://127.0.0.1:8080/check_file/{address}').text
    if not target:
        time.sleep(1)
        return redirect('/')

    return render_template('file.html', address=address,
                           name='<html><head><title>Burp Suite Professional</title> <style type="text/css"> body { background: #dedede; font-family: Arial, sans-serif; color: #404042; -webkit-font-smoothing: antialiased; } #container { padding: 0 15px; margin: 10px auto; background-color: #ffffff; } a { word-wrap: break-word; } a:link, a:visited { color: #e06228; text-decoration: none; } a:hover, a:active { color: #404042; text-decoration: underline; } h1 { font-size: 1.6em; line-height: 1.2em; font-weight: normal; color: #404042; } h2 { font-size: 1.3em; line-height: 1.2em; padding: 0; margin: 0.8em 0 0.3em 0; font-weight: normal; color: #404042;} .title, .navbar { color: #ffffff; background: #e06228; padding: 10px 15px; margin: 0 -15px 10px -15px; overflow: hidden; } .title h1 { color: #ffffff; padding: 0; margin: 0; font-size: 1.8em; } div.navbar {position: absolute; top: 18px; right: 25px;} div.navbar ul {list-style-type: none; margin: 0; padding: 0;} div.navbar li {display: inline; margin-left: 20px;} div.navbar a {color: white; padding: 10px} div.navbar a:hover, div.navbar a:active {text-decoration: none; background: #404042;} </style> </head> <body> <div id="container"> <div class="title"><h1>Burp Suite Professional</h1></div> <h1>Error</h1><p>Invalid&#32;client&#32;request&#32;received&#58;&#32;First&#32;line&#32;of&#32;request&#32;did&#32;not&#32;contain&#32;an&#32;absolute&#32;URL&#32;&#45;&#32;try&#32;enabling&#32;invisible&#32;proxy&#32;support&#46;</p> <div class="request">GET&nbsp;/check_file/' + address + '&nbsp;HTTP/1.1<br> Host:&nbsp;127.0.0.1:666<br> User-Agent:&nbsp;python-requests/2.28.2<br> Accept-Encoding:&nbsp;gzip,&nbsp;deflate,&nbsp;br<br> Accept:&nbsp;*/*<br> Connection:&nbsp;keep-alive<br> <br> </div><p>&nbsp;</p> </div> </body> </html>')


@app.route('/storage/<path:filename>')
def download_file(filename):
    try:
        return send_from_directory('./storage', filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)


utils.reset_storage()

if __name__ == "__main__":
    app.run('127.0.0.1', 8080, threaded=True)
