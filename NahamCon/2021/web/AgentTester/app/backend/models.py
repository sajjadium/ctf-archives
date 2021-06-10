from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000), unique=False)
    about = db.Column(db.String(1000), unique=False)

    def __str__(self):
        return self.username

    def get_user_id(self):
        return self.id
