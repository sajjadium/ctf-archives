from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship, backref
from flask_marshmallow import Marshmallow

import uuid

from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(120))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Note(db.Model):
    __tablename__ = 'note'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(50))
    content = Column(String(100))
    owner_id = Column(Integer, ForeignKey('user.id'))
    
    owner = relationship(
        User,
        backref=backref(
            'user',
            uselist=True,
            cascade='delete,all'
        )
    )


ma = Marshmallow()
class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note