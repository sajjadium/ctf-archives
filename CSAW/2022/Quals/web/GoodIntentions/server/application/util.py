import os
from flask import current_app, abort
from flask_login import current_user
import functools

generate = lambda x: os.urandom(x).hex()

def admin_only(f):
    @functools.wraps(f)
    def wrap(*args, **kwargs):
        if current_user.username == current_app.config['ADMIN_USERNAME']:
            return f(*args, **kwargs)
        else:
            return abort(401)
    return wrap
