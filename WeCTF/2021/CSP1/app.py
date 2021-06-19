import urllib.parse
import uuid

from flask import Flask, render_template, request, redirect, make_response
from bs4 import BeautifulSoup as bs
from peewee import *


app = Flask(__name__)

db = SqliteDatabase("core.db")


class Post(Model):
    id = AutoField()
    token = CharField()
    content = TextField()

    class Meta:
        database = db


@db.connection_context()
def initialize():
    db.create_tables([Post])


initialize()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/write', methods=["POST"])
def write():
    content = request.form["content"]
    token = str(uuid.uuid4())
    Post.create(token=token, content=content)
    return redirect("/display/" + token)


def filter_url(urls):
    domain_list = []
    for url in urls:
        domain = urllib.parse.urlparse(url).scheme + "://" + urllib.parse.urlparse(url).netloc
        if domain:
            domain_list.append(domain)
    return " ".join(domain_list)


@app.route('/display/<token>')
def display(token):
    user_obj = Post.select().where(Post.token == token)
    content = user_obj[-1].content if len(user_obj) > 0 else "Not Found"
    img_urls = [x['src'] for x in bs(content).find_all("img")]
    tmpl = render_template("display.html", content=content)
    resp = make_response(tmpl)
    resp.headers["Content-Security-Policy"] = "default-src 'none'; connect-src 'self'; img-src " \
                                              f"'self' {filter_url(img_urls)}; script-src 'none'; " \
                                              "style-src 'self'; base-uri 'self'; form-action 'self' "
    return resp


if __name__ == '__main__':
    app.run()
