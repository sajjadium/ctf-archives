from flask import Flask, render_template, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["120/minute"]
)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    return 'Under Construction...'


@app.route('/flag')
def flag():
    with open('flag', 'r') as f:
        return f.read()


@app.errorhandler(429)
def ratelimit_handler(e):
    return 'If you keep that request rate, you will are only contributing the climate change. Respect <a href=\"https://www.youtube.com/watch?v=0YPC6sfgj2I\">our environment</a> and find smarter solutions'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

