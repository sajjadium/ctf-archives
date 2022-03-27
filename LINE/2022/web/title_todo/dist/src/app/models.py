from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey, UniqueConstraint, Text, DateTime
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import current_timestamp

import uuid

from database import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password_hash = Column(String(120))
    is_admin = Column(Boolean, default=False)

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


class Image(db.Model):
    __tablename__ = 'image'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(Text)
    url = Column(Text)
    owner_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    
    owner = relationship(
        User,
        backref=backref(
            'image_owner',
            uselist=True,
            cascade='delete,all'
        )
    )


class Share(db.Model):
    __tablename__ = 'share'
    __table_args__ = (UniqueConstraint('image_id', 'shared_user_id'),)

    id = Column(Integer, primary_key=True)
    image_id = Column(UUIDType(binary=False), ForeignKey('image.id'))
    shared_user_id = Column(Integer, ForeignKey('user.id'))

    image = relationship(
        Image,
        backref=backref(
            'image',
            uselist=True,
            cascade='delete,all'
        )
    )

    shared_user = relationship(
        User,
        backref=backref(
            'shared_user',
            uselist=True,
            cascade='delete,all'
        )
    )