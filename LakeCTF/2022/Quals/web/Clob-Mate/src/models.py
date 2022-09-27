from . import db

class Order(db.Model):
    order_id = db.Column(db.Text(), primary_key=True)
    email = db.Column(db.Text())
    username = db.Column(db.Text())
    quantity = db.Column(db.Text())
    address = db.Column(db.Text())
    article = db.Column(db.Text())
    status = db.Column(db.Text())