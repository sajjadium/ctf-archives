from flask import Flask, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from redis import Redis
from rq import Queue
from werkzeug.exceptions import HTTPException
import os

db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)

q = Queue(connection=Redis.from_url('redis://redis:6379'))


def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return render_template('error.html', e=e), code


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_error_handler(Exception, handle_error)
    
    limiter.init_app(app)

    db.init_app(app)
    from .models import Order
    db.create_all(app=app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app