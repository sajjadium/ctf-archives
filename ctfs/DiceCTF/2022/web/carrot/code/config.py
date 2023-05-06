import secrets
import os

SECRET_KEY = secrets.token_hex(32)
MAX_CONTENT_LENGTH = 1048576

ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', default='default_admin_password')