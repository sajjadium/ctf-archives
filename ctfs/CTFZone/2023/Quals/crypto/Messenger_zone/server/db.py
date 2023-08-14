from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))



Base = declarative_base()

engine = create_engine("sqlite:///" + os.path.join(BASE_DIR, 'messages.db'))

if not database_exists(engine.url):
    print("Database does not exist")
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()