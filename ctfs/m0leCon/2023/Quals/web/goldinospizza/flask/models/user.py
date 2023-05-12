from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask_login import UserMixin
from server import db
from sqlalchemy.orm.attributes import flag_modified

hasher = PasswordHasher()


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Unicode, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Numeric, nullable=False, default=30)

    def get_id(self):
        return str(self.id)

    @classmethod
    def exists(cls, username):
        with db.Session(db.engine) as session:
            return session.execute(db.select(cls).filter(cls.username == username)).scalars().one_or_none() is not None

    @classmethod
    def register(cls, username, password):
        with db.Session(db.engine) as session:
            user = session.execute(db.select(cls).filter(
                cls.username == username)).scalars().one_or_none()
            if user is None:
                user = cls(username=username)
                session.add(user)
            user.password = hasher.hash(password)
            flag_modified(user, "password")
            session.commit()
        return user

    def verify(self, password):
        try:
            hasher.verify(self.password, password)
        except VerifyMismatchError:
            return False
        if hasher.check_needs_rehash(self.password):
            with db.Session(db.engine) as session:
                self.password = hasher.hash(password)
                flag_modified(self, "password")
                session.commit()
        return True
