from flask_sqlalchemy import SQLAlchemy
from retrying import retry

db = SQLAlchemy()

@retry(wait_fixed=2000, stop_max_attempt_number=10)
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()