from . import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.String(16), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fullname = db.Column(db.Text())
    title = db.Column(db.Text())
    lab = db.Column(db.Text())
    bio = db.Column(db.Text())
