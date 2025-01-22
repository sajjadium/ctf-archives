from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder='/app/app/static')
    app.config.from_object("config.Config")
    os.makedirs(os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].split('sqlite:///')[1]), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    db.init_app(app)
    Session(app)

    with app.app_context():
        from . import routes
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization failed: {e}")
            raise

    return app