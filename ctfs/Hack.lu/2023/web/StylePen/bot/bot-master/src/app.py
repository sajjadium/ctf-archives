#!/usr/bin/env python

from curses.ascii import SI
import os, stat
import sys
import re
import datetime
from urllib.parse import urlparse, urlunparse
from flask import Flask, request, render_template, jsonify

import log
import config
import worker

PORT = int(os.getenv('PORT', '5000'))
BIND_ADDR = os.getenv('BIND_ADDR', '127.0.0.1')
PASSWORD = os.getenv('SHARED_SECRET') or "secret"
ORIGIN = os.getenv('ORIGIN') if os.getenv('ORIGIN') and os.getenv('ORIGIN') != "http://localhost" else 'http://stylepen'
LOGIN_URL = ORIGIN + os.getenv('LOGIN_PATH')
LOGIN_CHECK = os.getenv('LOGIN_CHECK')

app = Flask(__name__)

def create_app():
    stat_info = os.stat("/var/run/docker.sock")
    if stat.S_IFMT(stat_info.st_mode) != stat.S_IFSOCK:
        print("Docker socket not found, check volume mounts in docker-compose.yml")
        return None
    return app

@app.route('/', methods=['POST'])
def index():
    global config

    json = request.json
    if json["secret"] != PASSWORD:
        return jsonify("Wrong secret")
    
    link = json['link']
    if not link:
        return jsonify("No link")

    # makes local testing less confusing
    parsed_url = urlparse(link)
    if parsed_url.hostname == "localhost":
        new_parsed_url = parsed_url._replace(netloc="stylepen")
        link = urlunparse(new_parsed_url)

    if re.search(f"^{ORIGIN}/.*", link) is None:
        log.log("[flask]", f"Invalid link {link}")
        return jsonify(f"Invalid link. link pattern: ^{ORIGIN}/.*")

    # spawn bot
    task = (link, { "user": json["username"], "password": PASSWORD, "loginUrl": LOGIN_URL, "loginCheck": LOGIN_CHECK })
    worker.add_task(task)

    return jsonify("ok")


@app.route('/info', methods=['GET'])
def info():
    return {
        'queue_size': worker.queue_size(),
        'worker_count': config.config['worker_count'],
        'timeout_secs': config.config['timeout_secs'],
        'use_recaptcha': config.config['use_recaptcha'],
        'timestamp': datetime.datetime.now().isoformat()
    }



def main(config_file):
    config.init_config(config_file)

    app.run(host=BIND_ADDR, port=PORT) # debug=True
    
    # shutdown
    worker.kill_all_workers()
    config.stop_config_loader()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} <config.json>'.format(sys.argv[0]))
        exit(1)

    main(sys.argv[1])

elif __name__ == 'app':
    # we are in gunicorn, so just load the config
    config.init_config('./config.json')
