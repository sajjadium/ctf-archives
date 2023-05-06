from flask_login import UserMixin
from . import globals


class User(globals.Database.Model, UserMixin):
    id = globals.Database.Column(globals.Database.Integer, primary_key=True)
    username = globals.Database.Column(globals.Database.String(64),  nullable=False)
    password = globals.Database.Column(globals.Database.String(32), nullable=False)
    level = globals.Database.Column(globals.Database.Integer, nullable=False)

    def __init__(self, username, password, level=1):
        self.username = username
        self.level = level
        self.password = self.hash_password(password)

    def hash_password(self, pwd):
        k = globals.App.config["SECRET_KEY"]
        pwd = bytearray(pwd, encoding='latin1')
        for i in range(0, len(pwd)):
            pwd[i] ^= ord(k[(i + self.level) % len(k)])
        return pwd.hex()

    @property
    def is_admin(self):
        return self.level == 10

    @property
    def is_moderator(self):
        return self.level == 8

    @property
    def is_user(self):
        return self.level == 1

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.username


class LoginLog(globals.Database.Model):
    id = globals.Database.Column(globals.Database.Integer, primary_key=True)
    username = globals.Database.Column(globals.Database.String(64),  nullable=False)
    ip = globals.Database.Column(globals.Database.String(64),  nullable=False)
    time = globals.Database.Column(globals.Database.DateTime, nullable=False)
    success = globals.Database.Column(globals.Database.Boolean, nullable=False)

    def __init__(self, username, ip, time, success):
        self.username = username
        self.ip = ip
        self.time = time
        self.success = success

    def __repr__(self):
        return '<LoginLog %r>' % self.username
