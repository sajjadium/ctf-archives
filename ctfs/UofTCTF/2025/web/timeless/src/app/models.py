import uuid
from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    profile_photo = db.Column(db.String(120), nullable=True)
    posts = db.relationship('BlogPost', backref='author', lazy=True)
    about_me = db.Column(db.Text, nullable=True)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid.uuid1()))
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)
    visibility = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)