from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://{username}:{password}@{host}:{port}/catgle".format(
                                                username=os.environ['MYSQL_USER'],
                                                password=os.environ['MYSQL_PASSWORD'],
                                                host=os.environ['MYSQL_HOST'],
                                                port=os.environ['MYSQL_PORT'])

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'connect_timeout': 20}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s'
}
Base.metadata = MetaData(naming_convention=naming_convention)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
