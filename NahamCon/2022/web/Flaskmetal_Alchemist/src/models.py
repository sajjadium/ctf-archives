from database import Base
from sqlalchemy import Column, Integer, String


class Metal(Base):
    __tablename__ = "metals"
    atomic_number = Column(Integer, primary_key=True)
    symbol = Column(String(3), unique=True, nullable=False)
    name = Column(String(40), unique=True, nullable=False)

    def __init__(self, atomic_number=None, symbol=None, name=None):
        self.atomic_number = atomic_number
        self.symbol = symbol
        self.name = name


class Flag(Base):
    __tablename__ = "flag"
    flag = Column(String(40), primary_key=True)

    def __init__(self, flag=None):
        self.flag = flag
