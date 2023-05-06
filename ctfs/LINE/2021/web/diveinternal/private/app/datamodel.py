import os
from datetime import date, datetime, timedelta
from sqlalchemy import create_engine, ForeignKeyConstraint
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, String, Integer, Date, Table, Boolean, ForeignKey, DateTime, BLOB, Text, JSON, Float
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Database:
    SQLITE = 'sqlite'
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }
    # Main DB Connection Ref Obj
    dbEngine = None

    sdbType = SQLITE
    if sdbType in DB_ENGINE.keys():
        engineUrl = DB_ENGINE[sdbType].format(DB=os.environ['DBFILE'])
        dbEngine = create_engine(engineUrl,connect_args={'check_same_thread': False})
        session = sessionmaker(bind=dbEngine,expire_on_commit=False)

    else:
        print("DBType is not found in DB_ENGINE")

class Subscriber(Base):
    __tablename__ = 'Subscriber'
    id = Column(Integer, primary_key=True)

    email = Column(String)
    date = Column(String)

    def __init__(self, email, date):
        self.email = email
        self.date = date
