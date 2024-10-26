from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis

from secrets import token_hex
from os import getenv

db = SQLAlchemy()
login_manager = LoginManager()
redis_client = Redis(
    host=getenv("REDIS_HOST"),
    port=int(getenv("REDIS_PORT")),
)

class TestConfig:
    DEBUG = True
    DEVELOPMENT = True

    BLOG_NAME = "Blogodogo"
    REFERRAL_CODE = getenv("REFERRAL_CODE")

    # SERVER_NAME = "localhost.localdomain"
    SECRET_KEY = token_hex()
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
