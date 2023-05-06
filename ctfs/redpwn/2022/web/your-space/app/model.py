from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    _password = db.Column(db.String(96), nullable=False)
    webhook = db.Column(db.String(96), nullable=False, default="")
    spaces = db.relationship("Space", backref="user", lazy=True)
    subscriptions = db.relationship("Subscription", backref="user", lazy=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = generate_password_hash(password)

    @staticmethod
    @login.user_loader
    def get_by_id(user_id):
        return User.query.get(int(user_id))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    space_id = db.Column(db.Integer, db.ForeignKey("space.id"))


class Space(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    name = db.Column(db.String(32), nullable=False, default="")
    posts = db.relationship("Post", backref="space", lazy=True)
    subscriptions = db.relationship("Subscription", backref="space", lazy=True)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    space_id = db.Column(db.Integer, db.ForeignKey("space.id"), nullable=False)
    content = db.Column(db.Text(), nullable=False, default="")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
