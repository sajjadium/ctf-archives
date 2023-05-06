import os


class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "RedisCache"
    WTF_CSRF_ENABLED = False


class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    CACHE_REDIS_URL = "redis://redis:6379/0"


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "secret key"
    CACHE_REDIS_URL = "redis://localhost:6379/0"
