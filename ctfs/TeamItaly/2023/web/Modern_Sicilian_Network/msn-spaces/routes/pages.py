import re
import uuid
import timeago
import logging
from datetime import datetime
from flask import Blueprint, request, session, redirect, render_template
from utils.models import *
from utils.auth import *

DOMAIN = os.getenv("DOMAIN")
CHAT_PORT = os.getenv("CHAT_PORT")

bp = Blueprint("pages", __name__)

@bp.route("/")
def index():
    return render_template("welcome.html")

@bp.route("/login")
@request_auth # let's not waste logic lol
def login():
    return redirect("/")

@bp.route("/logout")
def logout():
    session.pop("id", None)
    session.pop("username", None)
    session.pop("propic", None)
    return redirect("/")


@bp.route("/articles/")
@request_auth
def showArticleMaker():
    return render_template("article-editor.html")


@bp.post("/articles/<userId>/")
@request_auth
def createArticle(userId):
    if userId != session["id"]:
        return render_template("error.html", message="You can only write an article for yourself."), 403
    try:
        data = request.form
        title = data["title"]
        content = data["content"]
        if len(title) > 128:
            return render_template("error.html", message="Title must be shorter than 128 characters.")
        if len(content) > 2048:
            return render_template("error.html", message="Article must be shorter than 2048 characters.")
        if Article.query.filter_by(author=userId, title=title).first():
            return render_template("error.html", message="You already used that title."), 409
        # let's filter scripts
        content = re.sub(r"(?s)<\s*(script)[\d\D]*?<\s*/\s*\1\s*>", "", content)
        articleId = str(uuid.uuid4())
        article = Article(articleId, userId, datetime.utcnow(), title, content)
        db.session.add(article)
        db.session.commit()
        return redirect(f"/articles/{userId}/{articleId}")
    except AttributeError as e:
        return render_template("error.html", message="Invalid request"), 400
    except Exception as e:
        logging.error(e)
        return render_template("error.html", message="Server error"), 500


@bp.route("/articles/<userId>/")
def showUserArticles(userId):
    user = User.query.get(userId)
    if not user:
        return render_template("error.html", message="This user doesn't exist."), 404
    articles = Article.query.filter_by(author=user.id)
    return render_template("article-list.html", user=user, articles=articles)


@bp.route("/articles/<userId>/<articleId>/")
def showArticle(userId, articleId):
    user = User.query.get(userId)
    if not user:
        return render_template("error.html", message="This user doesn't exist."), 404
    article = Article.query.filter_by(author=user.id, id=articleId).first()
    if not article:
        return render_template("error.html", message="This article doesn't exist."), 404
    articleTimestamp = timeago.format(article.timestamp, datetime.utcnow())
    return render_template(
        "article-view.html",
        user=user,
        title=article.title,
        text=article.content,
        timestamp=articleTimestamp,
        DOMAIN=DOMAIN,
        CHAT_PORT=CHAT_PORT
    )