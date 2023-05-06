from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__, static_folder='static')
app.config.update(
    SESSION_COOKIE_SECURE=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

limiter = Limiter(
    app,
    key_func=get_remote_address
)

login_manager = LoginManager()
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, db
from app.models import User, Consent
import os
from werkzeug.security import generate_password_hash

@app.before_first_request
def setup():
    flag = os.environ.get('FLAG') or 'justCTF{fake}'
    pwd = os.environ.get('PASSWD') or 'admin'
    if not User.query.filter_by(username=flag).first():
        user = User(username = flag, 
                    password_hash = generate_password_hash(pwd))
        db.session.add(user)
        db.session.commit()