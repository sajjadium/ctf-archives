from datetime import datetime
import os
import random
import uuid
class Config:
    JSON_SORT_KEYS = False
    START_TIME = datetime.now()
    random.seed(int(START_TIME.timestamp()))
    SECRET_KEY = str(uuid.uuid1(clock_seq=random.getrandbits(14)))
    SESSION_USE_SIGNER = True
    TEMPLATES_AUTO_RELOAD = False
    SESSION_PERMANENT = True
    SESSION_TYPE = 'filesystem'
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(os.getcwd(), 'db', 'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
