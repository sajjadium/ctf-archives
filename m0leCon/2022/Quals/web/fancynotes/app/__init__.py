import os
from time import sleep
from flask import Flask
from .db import db
from .routes import init_routes
from .models import *
from .utils import init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:////tmp/test.db',
    )
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

    if os.environ.get("DOCKER"):
        PASS = os.environ.get("MYSQL_ROOT_PASSWORD")
        DB = os.environ.get("MYSQL_DATABASE")
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:{PASS}@db/{DB}?charset=utf8mb4'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    with app.app_context():
        # Connect to database
        tries = 10
        while tries > 0:
            try:
                db.create_all()
                tries = 0
            except:
                tries += -1
                print('Failed to connect to database. Waiting and then trying again (try countdown: %s)' % tries)
                sleep(5)
        init_db(db)

    init_routes(app)

    return app
