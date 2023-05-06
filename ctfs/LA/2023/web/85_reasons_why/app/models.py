from app import db
from datetime import datetime

import uuid
import json


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.String(36), primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    images = db.relationship("Image", backref="post", uselist=True)
    comments = db.relationship("Comment", backref="post", uselist=True)

    def __init__(self, title, content, author):
        self.id = str(uuid.uuid4())
        self.title = title
        self.content = content
        self.author = author
        self.date = datetime.now().strftime("%m-%d-%Y, %H:%M:%S")
        self.active = True


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.String(36), primary_key=True)
    author = db.Column(db.String(144), nullable=False)
    comment = db.Column(db.String(144), nullable=False)
    parent = db.Column(db.String(), db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, author, comment):
        self.id = str(uuid.uuid4())
        self.author = author
        self.comment = comment

    def __repr__(self):
        return f'<Comment {self.comment}>'


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(36), primary_key=True)
    b85_image = db.Column(db.String(1000000))
    parent = db.Column(db.String(), db.ForeignKey("posts.id"), nullable=False)

    def __init__(self, b85_image):
        self.id = str(uuid.uuid4())
        self.b85_image = b85_image
    
    def __repr__(self):
        return f'<Image {self.id}>'
