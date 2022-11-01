#!/usr/bin/env python

from curses.ascii import SI
import os
import re
import sys
import datetime
from flask import Flask, request, render_template

import config
import worker
import recaptcha

PORT = int(os.getenv('PORT', '5000'))
BIND_ADDR = os.getenv('BIND_ADDR', '127.0.0.1')
ADMIN_PASS = os.getenv('ADMIN_PASSWORD')
LOGIN_URL = os.getenv('LOGIN_URL')
LOGIN_CHECK = os.getenv('LOGIN_CHECK')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global config
    msg = ''
    error = ''

    if request.method == 'POST':
        link = request.form.get('link')

        # check recaptcha
        if config.config['use_recaptcha']:
            recaptcha_secret_key = config.config.get('recaptcha_secret_key', None)
            recaptcha_response = request.form.get('recaptcha')
            captcha_ok = recaptcha.verify(recaptcha_secret_key, recaptcha_response)
        else:
            captcha_ok = True


        # check link, level and captcha
        if(re.search(config.config['link_pattern'], link) and captcha_ok):
            # spawn admin bot
            print('[+] Spawning Admin Bot')
            task = (link, )
            position = worker.add_task(task)
            msg = 'We will have a look. You are at position {} in the queue.'.format(position)
        else:
            error = 'Error!'

    return render_template('index.html',
        use_recaptcha=config.config['use_recaptcha'],
        recaptcha_public_key=config.config.get('recaptcha_public_key', None),
        link_pattern=config.config['link_pattern'],
        msg=msg,
        error=error,
    )

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
