from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from config import db


class Authors(db.Model, UserMixin):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), unique=False, nullable=False)
 
    register_date = db.Column(db.DateTime(), unique=False, default=datetime.now())
    admin = db.Column(db.Boolean, default=False)
 
    url = db.Column(db.String(128), unique=False, nullable=True, default="")
    avatar = db.Column(db.String(64), unique=False, nullable=True, default=None)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Posts(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False, unique=False)
    subtitle = db.Column(db.String(128), nullable=False, unique=False)
    slug = db.Column(db.String(64), nullable=False, unique=True)
    content = db.Column(db.String(512), nullable=False, unique=False)
 
    draft = db.Column(db.Boolean, default=True)
    hash_preview = db.Column(db.String(64), nullable=False, unique=True)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))
