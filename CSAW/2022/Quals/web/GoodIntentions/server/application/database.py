from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import current_app

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

class Image(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    location = db.Column(db.String(100), unique=True)

def clear_db():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

def migrate_db():
    clear_db()

    # admin user
    db.session.add(User(id=1, username=current_app.config['ADMIN_USERNAME'], password=current_app.config['ADMIN_PASSWORD']))
    db.session.commit()