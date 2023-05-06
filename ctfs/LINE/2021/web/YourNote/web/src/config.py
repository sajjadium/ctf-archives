import os

class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'


class DevConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev.sqlite3'
    SECRET_KEY = 'dev_secret'
    ADMIN_PASSWORD = 'password'
    FLAG = 'LINECTF{example}'
    APP_HOST = 'localhost:5000'
    BASE_URL = f"http://{APP_HOST}"
    CRAWLER_URL = 'http://localhost:3000'
    POW_COMPLEXITY = 1

class ProdConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"mysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@yournote-db/{os.getenv('MYSQL_DATABASE')}"
    SECRET_KEY = os.getenv('SECRET_KEY')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
    FLAG = os.getenv('FLAG')
    APP_HOST = os.getenv('APP_HOST')
    BASE_URL = f"http://{APP_HOST}"
    CRAWLER_URL = os.getenv('CRAWLER_URL')
    POW_COMPLEXITY = os.getenv('POW_COMPLEXITY')
