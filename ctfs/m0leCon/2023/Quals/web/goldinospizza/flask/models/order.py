from server import db


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(
        "product.id"), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.Numeric, nullable=False)
    product = db.relationship("Product")

    def _asdict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "product_quantity": self.product_quantity,
            "product_price": self.product_price,
            "product": self.product._asdict(),
        }
