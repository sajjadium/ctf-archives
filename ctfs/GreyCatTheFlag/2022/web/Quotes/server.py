import random
from threading import Thread

import os
import requests
import time
from secrets import token_hex

from flask import Flask, render_template, make_response, request
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium import webdriver


app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')

sockets = Sockets(app)

auth_token = token_hex(64)

quotes=requests.get("https://gist.githubusercontent.com/robatron/a66acc0eed3835119817/raw/0e216f8b6036b82de5fdd93526e1d496d8e1b412/quotes.txt").text.rstrip().split("\n")


# best way to get rid of chromium Ndays is to use firefox instead
DRIVER_PATH = "/app/geckodriver"

options = Options()
options.headless = True


class Bot(Thread):
    def __init__(self, url):
        Thread.__init__(self)
        self.url = url

    def run(self):
        driver = webdriver.Firefox(service=Service(DRIVER_PATH), options=options)
        driver.get(self.url)
        time.sleep(3)
        driver.quit()


@app.route('/')
def start():
    return render_template('index.html')


# authenticate localhost only
@app.route('/auth')
def auth():
    print('/auth', flush=True)
    print(request.remote_addr, flush=True)
    if request.remote_addr == "127.0.0.1":
        resp = make_response("authenticated")
        # I heard httponly defend against XSS(what is that?)
        resp.set_cookie("auth", auth_token, httponly=True)
    else:
        resp = make_response("unauthenticated")
    return resp


@sockets.route('/quote')
def echo_socket(ws):
    print('/quote', flush=True)
    while not ws.closed:
        try:
            try:
                cookie = dict(i.split('=') for i in ws.handler.headers.get('Cookie').split('; '))
            except:
                cookie = {}

            # only admin from localhost can get the GreyCat's quote
            if ws.origin.startswith("http://localhost") and cookie.get('auth') == auth_token:
                ws.send(f"{os.environ['flag']}")
            else:
                ws.send(f"{quotes[random.randint(0,len(quotes))]}")
            ws.close()
        except Exception as e:
            print('error:',e, flush=True)

@app.route('/share', methods=['GET','POST'])
def share():
    if request.method == "GET":
        return render_template("share.html")
    else:
        if not request.form.get('url'):
            return "yes?"
        else:
            thread_a = Bot(request.form.get('url'))
            thread_a.start()
            return "nice quote, thanks for sharing!"


if __name__ == "__main__":
    try:
        server = pywsgi.WSGIServer(('0.0.0.0', 7070), application=app, handler_class=WebSocketHandler)
        print("web server start ... ", flush=True)
        server.serve_forever()
    except Exception as e:
        print('error:',e, flush=True)

