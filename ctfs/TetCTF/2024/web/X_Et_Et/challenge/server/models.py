from app import db

class User(db.Model):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50))

# Define the Ticket model
class Ticket(db.Model):
    id = db.Column(db.String(36), primary_key=True, unique=True)
    title = db.Column(db.String(100))
    new = db.Column(db.Integer)
    content = db.Column(db.Text)
    username = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    