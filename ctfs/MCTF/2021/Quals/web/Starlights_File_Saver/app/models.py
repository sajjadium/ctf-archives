from flask_login import UserMixin
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from dataclasses import dataclass


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@dataclass
class File(db.Model):
    id: int
    filename: str

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(32))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
