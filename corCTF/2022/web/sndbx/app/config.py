import os
from datetime import timedelta

SESSION_TYPE = 'filesystem'
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_DOMAIN = False
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, 'templates/')
MAX_CONTENT_LENGTH = 1024 * 500

SERVER_NAME = DOMAIN = os.environ['DOMAIN']

PORT = 443