from flask import Flask
from flask_sessionstore import Session
from flask_login import LoginManager
from flask_caching import Cache
from . import globals
from dotenv import load_dotenv

Login = LoginManager()


def create_app(name, config=None):
    load_dotenv()
    globals.App = Flask(name)

    if config is not None:
        globals.App.config.from_object(config)
    else:
        globals.App.config.from_pyfile("app/config.py")

    with globals.App.app_context():
        globals.Cache = Cache(globals.App)
        Login.init_app(globals.App)
        globals.Session = Session(globals.App)
        globals.Session.app.session_interface.db.create_all()
        from . import database
        admin_usr, admin_pwd = database.init_database(globals.App)
        from . import routes
        routes.init_routes(globals.App)

    return globals.App, admin_usr, admin_pwd
