from flask import Flask, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin
from flask_sock import Sock
from redis import Redis
from rq import Queue
from werkzeug.exceptions import HTTPException
import secrets
import os

limiter = Limiter(key_func=get_remote_address)

q = Queue(connection=Redis.from_url('redis://redis:6379'))

admin_token = os.getenv('ADMIN_TOKEN') or secrets.token_hex()

sock = Sock()


class User(UserMixin):
    def __init__(self, id):
        self.id = id


def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html', e=e), code


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    app.register_error_handler(Exception, handle_error)

    limiter.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        if user_id == 'admin':
            return User('admin')
    
    @app.after_request
    def add_header(response):
        response.headers["Content-Security-Policy"] = "default-src 'none'; script-src 'self'; frame-src *; style-src 'self'; font-src 'self' https://*.epfl.ch; img-src * data:; connect-src 'self'"
        response.headers["X-Frame-Options"] = "DENY"
        return response


    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    sock.init_app(app)

    app.counter = 1337

    return app
