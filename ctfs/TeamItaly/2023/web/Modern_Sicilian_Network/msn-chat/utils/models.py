from argon2 import PasswordHasher
from .db import db

ALLOWED_LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!$-.@^_~"
PROPIC_BASE = "/static/propic"
ALLOWED_PROPICS = [
    "cannoli.jpg",
    "iris.jpg",
    "pane-e-panelle.jpg",
    "arancina.jpg",
    "tofu.png",
    "tofu-tongue.jpg",
    "tofu-knows-what-you-are.jpg",
    "tofu-blanket.jpg"
]

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(128))
    propic = db.Column(db.String(32))
    powTarget = db.Column(db.String(64))

    def __init__(self, id, username, password, propic="tofu"):
        ph = PasswordHasher(memory_cost=2048)
        self.id = id
        self.username = username
        self.password = ph.hash(password)
        self.propic = propic
        self.powTarget = ""

    def __repr__(self):
        return f"<User {self.username!r}>"


class Message(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    type = db.Column(db.SmallInteger)
    content = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime())
    receiver_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    receiver = db.relationship("User", backref=db.backref("messages", lazy='dynamic'), primaryjoin="User.id == Message.receiver_id")
    sender_id = db.Column(db.String(36), db.ForeignKey("user.id"), nullable=False)
    sender = db.relationship("User", backref=db.backref("sent", lazy=True), primaryjoin="User.id == Message.sender_id")

    def __init__(self, id, type, content, timestamp, receiver, sender):
        self.id = id
        self.type = type
        self.content = content
        self.timestamp = timestamp
        self.receiver_id = receiver.id
        self.receiver = receiver
        self.sender_id = sender.id
        self.sender = sender

    def __repr__(self):
        return f"<Message {self.content!r}>"


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