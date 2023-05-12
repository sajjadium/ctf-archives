from server import db


class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    description = db.Column(db.Unicode, nullable=True)
    image = db.Column(db.Unicode, nullable=True)
    theme = db.Column(db.Unicode, nullable=True)

    def _asdict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "description": self.description,
            "image": self.image,
            "theme": self.theme,
        }
