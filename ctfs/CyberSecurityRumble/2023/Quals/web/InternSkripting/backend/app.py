from flask import Flask
from flask import request
import logging
import os
import json

app = Flask(__name__)

flag = os.getenv("flag", "not_the_real_thing")

def represents_int(s, default):
    try: 
        app.logger.info("int %s", s)
        return int(s, 0)
    except:
        return default


@app.route("/flag")
def get_flag():
    coffee_secret = request.headers.get('X-Coffee-Secret')
    coffee_disallow = request.headers.get('X-Coffee-Disallow', None)
    coffee_debug = request.headers.get('X-Coffee-Debug', None)
    app.logger.info(request.headers)
    app.logger.info("header contents %s %s %s", coffee_secret, coffee_disallow, coffee_debug)
    app.logger.info("int %d", represents_int(coffee_disallow, 1))
    if represents_int(coffee_disallow, 1) != 0 :
        return json.dumps({"value": "Filthy coffee thief detected!", "code": 418}), 418
    app.logger.info("Gave coffee flag to someone with the secret %s", coffee_secret)
    return json.dumps({"value": flag, "code": 200}), 200


@app.route("/")
def index():
    return json.dumps({"value": "To get a coffee flag go to /flag", "code": 200}), 200

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)