from flask_sqlalchemy import SQLAlchemy
from . import globals
import string
import random


def random_string(count=32):
    charset = string.digits + string.ascii_lowercase + string.ascii_uppercase
    pwd = ""
    for _ in range(0, count):
        pwd += random.choice(charset)
    return pwd


def init_database(app):
    globals.Database = SQLAlchemy(app)
    from .models import User
    globals.App.config["SESSION_SQLALCHEMY"] = globals.Database
    globals.Database.create_all()

    u = User.query.filter_by(username="admin").first()
    # delete the admin user if it exists
    if u is not None:
        globals.Database.session.delete(u)
        globals.Database.session.commit()
    # add the admin user
    admin_usr = "admin"
    admin_pwd = random_string(32)
    u = User(username=admin_usr, password=admin_pwd, level=10)
    globals.Database.session.add(u)
    globals.Database.session.commit()

    u = User.query.filter_by(username="jonathan").first()
    if u is None:
        user = User("jonathan", random_string(32), 1)
        globals.Database.session.add(user)
        globals.Database.session.commit()

    return admin_usr, admin_pwd

