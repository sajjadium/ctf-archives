from pathlib import Path

from flask import Flask
from flask_caching import Cache
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .notify import start_notifier

cache = Cache()
db = SQLAlchemy()
login = LoginManager()
login.login_view = "auth.login"
login.login_message = "not logged in"

flag_path = Path(__file__).parent / "flag.txt"
assert flag_path.is_file()
flag = flag_path.read_text().strip()


def create_app():
    app = Flask(__name__)

    if app.env == "production":
        app.config.from_object("app.config.ProdConfig")
        flag_path.unlink()
    else:
        app.config.from_object("app.config.DevConfig")

    cache.init_app(app)
    db.init_app(app)
    login.init_app(app)

    from .routes import auth, main, space

    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(space)

    with app.app_context():
        db.create_all()

    start_notifier()

    return app
