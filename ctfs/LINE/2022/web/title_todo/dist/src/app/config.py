import os
import secrets

class Config(object):
    SECRET_KEY = secrets.token_bytes()
    FLAG = os.getenv('FLAG')
    APP_HOST = os.getenv('APP_HOST')
    BASE_URL = f"http://{APP_HOST}/"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    UPLOAD_FOLDER = './static/image'
    REDIS_HOST = os.getenv('REDIS_HOST')
    REDIS_PORT = 6379
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')