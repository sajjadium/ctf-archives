import os
import uuid
from datetime import datetime
from functools import wraps
from flask import Blueprint, Response, request, session
from argon2.exceptions import VerifyMismatchError
from utils.db import db
from utils.models import *
from hashlib import sha256
import logging

API_PATH = "/api/v1"
SPACES_PORT = os.getenv("SPACES_PORT")

bp = Blueprint("api", __name__)

# auth wrapper
def request_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return "", 401
        return f(*args, **kwargs)
    return wrapper


# get MSN Spaces port
@bp.get(f"{API_PATH}/spacesPort")
def get_spaces_port():
    return str(SPACES_PORT)


# get own info
@bp.get(f"{API_PATH}/session")
@request_auth
def get_own_info():
    user = User.query.get(session["id"])
    return {
        "id": user.id,
        "username": user.username,
        "propic": f"/static/propic/{user.propic}"
    }


# login
@bp.post(f"{API_PATH}/session")
def login():
    try:
        data = request.get_json()
        username = data["username"].strip()
        password = data["password"].strip()
        ph = PasswordHasher(memory_cost=2048)
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "", 401
        ph.verify(user.password, password)
        session["id"] = user.id
        session["username"] = user.username
        session["propic"] = user.propic
        return "", 201
    except AttributeError as e:
        return "", 400
    except VerifyMismatchError:
        return "", 401
    except Exception as e:
        logging.error(e)
        return "", 500


# register
@bp.post(f"{API_PATH}/users")
def register():
    try:
        data = request.get_json()
        username = data["username"].strip()
        password = data["password"].strip()
        propic = data["propic"].strip()
        if not password or not 4 <= len(password) <= 128 or not 4 <= len(username) <= 32 or \
                any([c not in ALLOWED_LETTERS for c in username]) or propic not in ALLOWED_PROPICS:
            return "", 400
        # abort if username is already used
        if User.query.filter_by(username=username).first():
            return "", 409
        user = User(str(uuid.uuid4()), username, password, propic)
        db.session.add(user)
        db.session.commit()
        # create admin's first message
        admin = User.query.filter_by(username="Loldemort").first()
        welcomeArticleId = Article.query.filter_by(author=admin.id, title="Welcome to MSN!").first().id
        message = Message(
            str(uuid.uuid4()),
            1,
            f"{admin.id}/{welcomeArticleId}",
            datetime.utcnow(),
            user,
            admin
        )
        db.session.add(message)
        db.session.commit()
        session["id"] = user.id
        session["username"] = user.username
        session["propic"] = user.propic # doesn't contain /static/propic
        res = Response(status=201)
        res.headers["Content-Location"] = f"{API_PATH}/session"
        return res
    except AttributeError as e:
        return "", 400
    except Exception as e:
        logging.error(e)
        return "", 500


# get someone's info
@bp.get(f"{API_PATH}/users/<uuid>")
def get_user_info(uuid):
    user = User.query.filter_by(id=uuid).first()
    if not user:
        return "", 404
    return {
        "id": user.id,
        "username": user.username,
        "propic": f"/static/propic/{user.propic}"
    }
    

@bp.route(f"{API_PATH}/search/<otherId>")
@request_auth
def search(otherId):
    query = request.args.get("query", None)
    if not query:
        return "", 400
    target = User.query.get(otherId)
    if not target:
        return "", 404
    asker = User.query.get(session["id"])
    output = []
    messages_received = set(asker.messages).intersection(set(target.sent))
    messages_sent = set(asker.sent).intersection(set(target.messages))
    messages = list(messages_received.union(messages_sent))
    for msg in messages:
        if msg.type == 0 and query in msg.content:
            output.append(msg.id)
    return output, 200 if len(output) != 0 else 404