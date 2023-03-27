import hashlib
from datetime import datetime
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User, Chall

def create_user(db: Session, user_create: UserCreate, ip_addr: str):
    """
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    uploaded_model = Column(Boolean, nullable=False)
    registered_ip = Column(String, unique=True, nullable=False)
    """
    db_user = User(username=user_create.username,
                    password=hashlib.sha3_512(bytes(user_create.password, 'utf-8')).hexdigest(),
                    uploaded_model=False,
                    registered_ip=ip_addr,
                    last_activity=datetime.now(),
                    participated=0,
                    ranking=0,
                    register_date=datetime.now()
                    )
    db.add(db_user)
    db.commit()

def get_user(db:Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.username == user_create.username)
    ).first()

def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(
        (User.username == username)
    ).first()

def get_user_by_id(db: Session, userid: int):
    return db.query(User).filter(
        (User.id == userid)
    ).first()

def get_user_by_ip(db: Session, ip_addr: str):
    return db.query(User).filter(
        (User.registered_ip == ip_addr)
    ).first()

def hash_password(passwd: str):
    return hashlib.sha3_512(bytes(passwd, 'utf-8')).hexdigest()

def add_participation(db: Session, user: User, category: str):
    new_value = user.participated
    new_value = new_value | 1 if category == 'classification' else new_value
    new_value = new_value | 2 if category == 'gan' else new_value
    user.participated = new_value
    db.add(user)
    db.commit()

def delete_participation(db: Session, user: User, category: str):
    new_value = user.participated
    new_value = new_value & ~1 if category == 'classification' else new_value
    new_value = new_value & ~2 if category == 'gan' else new_value
    user.participated = new_value
    db.add(user)
    db.commit()