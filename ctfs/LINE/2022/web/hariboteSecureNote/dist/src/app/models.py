import uuid

import werkzeug.security
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy_utils import UUIDType


from database import db


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True)
    display_name = Column(String(16))
    password_hash = Column(String(120))
    is_admin = Column(Boolean, default=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        self.password_hash = werkzeug.security.generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return werkzeug.security.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'<User {self.user_id}>'


class Note(db.Model):
    __tablename__ = 'note'

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(64))
    content = Column(String(400))
    author_id = Column(Integer, ForeignKey('user.id'))
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    author = relationship(
        User,
        backref=backref(
            'note_author',
            uselist=True,
            cascade='delete,all'
        )
    )
