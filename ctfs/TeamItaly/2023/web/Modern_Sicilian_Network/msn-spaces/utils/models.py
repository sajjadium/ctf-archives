from .db import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    propic = db.Column(db.String(20))
    powTarget = db.Column(db.String(64))

    def __repr__(self):
        return f"<User {self.username!r}>"


class Article(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    author = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.DateTime())
    title = db.Column(db.String(128))
    content = db.Column(db.String(2048))

    def __init__(self, id, author, timestamp, title, content):
        self.id = id
        self.author = author
        self.timestamp = timestamp
        self.title = title
        self.content = content

    def __repr__(self):
        return f"<Message {self.title!r}>"