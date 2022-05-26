from flask import request
import uuid
import base64
import hashlib
import string
import os
import random
from .models import *


SECRET_KEY = os.environ.get("SECRET_KEY")
FLAG = os.environ.get("FLAG")


def random_string(n):
    return ''.join(random.choices(string.printable, k=n))


def init_db(db):
    username = "admin"
    password = random_string(20)

    if User.query.filter_by(username=username).count() > 0:
        return

    user = User(username=username, password=hashlib.sha256(
        password.encode()).hexdigest(), locale='en'
    )
    note = Note(title="flag", body=FLAG)
    user.notes.append(note)
    db.session.add(user)
    db.session.commit()


def get_user():
    if not 'user' in request.cookies:
        return None

    cookie = base64.b64decode(request.cookies.get(
        'user')).decode('raw_unicode_escape')
    assert len(cookie.split('|')) == 2
    user_string = cookie.split('|')[0]
    signature_string = cookie.split('|')[1]

    if hashlib.sha256((SECRET_KEY + user_string).encode('raw_unicode_escape')).hexdigest() != signature_string:
        print("nope")
        return None

    user = serialize_user(user_string)
    return user


def generate_cookie(user):
    user_string = deserialize_user(user)
    signature_string = hashlib.sha256(
        (SECRET_KEY + user_string).encode('raw_unicode_escape')).hexdigest()
    cookie = base64.b64encode(
        (f'{user_string}|{signature_string}').encode('raw_unicode_escape')).decode()
    return cookie


def deserialize_user(user):
    values = []
    for k in ["username", "locale"]:
        values.append(f'{k}={user.__dict__[k]}')
    return ','.join(values)


def serialize_user(user_string):
    user = dict()
    for kv in user_string.split(','):
        k = kv.split('=')[0]
        v = kv.split('=')[1]
        user[k] = v
    return user


def save_picture(picture):
    if picture.filename == '':
        return None
    if '.' not in picture.filename and picture.filename.rsplit('.', 1)[1].lower() not in ['png', 'jpg', 'jpeg']:
        return None
    picture_id = uuid.uuid4().hex
    picture_path = os.path.join('/tmp/uploads', picture_id)
    picture.save(picture_path)
    return picture_id
