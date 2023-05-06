from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
from redis import Redis
from rq import Queue
from werkzeug.exceptions import HTTPException
import secrets
import os

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

q = Queue(connection=Redis.from_url('redis://redis:6379'))

admin_token = os.getenv('ADMIN_TOKEN') or secrets.token_hex()

def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html', e=e), code


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_error_handler(Exception, handle_error)

    csp = {
        'script-src': '',
        'object-src': "'none'",
        'style-src': "'self'",
        'default-src': ['*', 'data:']
    }
    Talisman(app,
        force_https=False,
        strict_transport_security=False,
        session_cookie_secure=False,
        content_security_policy=csp,
        content_security_policy_nonce_in=['script-src'])
    
    limiter.init_app(app)

    db.init_app(app)
    from .models import User
    db.create_all(app=app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app
