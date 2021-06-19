import os

from flask import Flask, render_template, request
from peewee import *

app = Flask(__name__)

db = SqliteDatabase("core.db")


class User(Model):
    id = AutoField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        database = db


@db.connection_context()
def initialize():
    try:
        db.create_tables([User])
        User.create(username="shou", password=os.getenv("FLAG"))
    except:
        pass


initialize()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    username = request.form["username"]
    password = request.form["password"]
    sql = f"INSERT INTO `user`(password, username) VALUES ('{password}', '{username}')"
    try:
        db.execute_sql(sql)
    except Exception as e:
        return f"Err: {sql} <br>" + str(e)
    return "Your password is leaked :)<br>" + \
           """<blockquote class="imgur-embed-pub" lang="en" data-id="WY6z44D"  ><a href="//imgur.com/WY6z44D">Please 
        take care of your privacy</a></blockquote><script async src="//s.imgur.com/min/embed.js" 
        charset="utf-8"></script> """


if __name__ == "__main__":
    app.run()

