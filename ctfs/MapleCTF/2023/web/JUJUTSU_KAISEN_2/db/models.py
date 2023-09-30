from database import db

class CharactersModel(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    cursed_technique = db.Column(db.String)
    img_file = db.Column(db.String)
    notes = db.Column(db.String)


