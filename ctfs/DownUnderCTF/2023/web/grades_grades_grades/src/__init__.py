from flask import Flask
from src.routes import api
from src import auth

def create_app():
    app = Flask(__name__)
    app.auth = auth
    app.register_blueprint(api)
    return app
