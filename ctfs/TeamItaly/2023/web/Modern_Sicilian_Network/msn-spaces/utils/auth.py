import os
from flask import session, redirect
from functools import wraps

DOMAIN = os.getenv("DOMAIN")
CHAT_PORT = os.getenv("CHAT_PORT")

# auth wrapper
def request_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return redirect(f"//chat.{DOMAIN}:{CHAT_PORT}/login?spaces")
        return f(*args, **kwargs)
    return wrapper