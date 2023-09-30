import uuid
import logging
from datetime import datetime
from flask import Blueprint, Response, redirect, request, session
from functools import wraps
from utils.db import db
from utils.models import *

API_PATH = "/api/v1"

bp = Blueprint("api", __name__)

# auth wrapper
def request_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "id" not in session:
            return "", 401
        return f(*args, **kwargs)
    return wrapper    

# get someone's articles
@bp.get(f"{API_PATH}/articles/<uuid>")
def list_user_articles(uuid):
    if not User.query.filter_by(id=uuid).first():
        return {}, 404
    json = []
    for article in Article.query.filter_by(author=uuid):
        json.append({
            "id": article.id,
            "title": article.title,
            "content": article.content,
            "timestamp": article.timestamp
        })
    return json

# get an article
@bp.get(f"{API_PATH}/articles/<uuid>/<article>")
def get_article(uuid, article):
    article = Article.query.filter_by(author=uuid, id=article).first()
    if not article:
        return "", 404
    user = User.query.filter_by(id=uuid).first()
    return {
        "author": {
            "username": user.username,
            "propic": f"/static/propic/{user.propic}"
        },
        "title": article.title,
        "content": article.content,
        "timestamp": article.timestamp
    }