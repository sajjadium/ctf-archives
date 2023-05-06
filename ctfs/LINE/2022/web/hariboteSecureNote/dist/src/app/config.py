import os
import secrets


class Config(object):
    APP_NAME = "Haribote Secure Note"
    BASE_URL = os.getenv('BASE_URL', 'http://nginx/')
    SECRET_KEY = secrets.token_bytes()

    RATELIMIT_HEADERS_ENABLED = True

    FLAG = os.getenv('FLAG', 'linectf{dummy}')

    REDIS_HOST = os.getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = os.getenv('REDIS_PORT', '6379')
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', '')

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USER_ID = os.getenv('ADMIN_USER_ID', 'admin')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'P@ssw0rd')

    NOTE_TITLE_MAX_LENGTH = 64
    NOTE_CONTENT_MAX_LENGTH = 128
    USER_DISPLAY_NAME_MAX_LENGTH = 16

    SHARE_ID_LENGTH = 64

    USER_ID_PATTERN = '^[a-zA-Z0-9-_]{1,50}$'

