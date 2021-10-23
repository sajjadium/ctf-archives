from flask import Flask
from config import Config
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
cache = Cache(app)
login = LoginManager(app)
from app import routes, models
db.create_all()
