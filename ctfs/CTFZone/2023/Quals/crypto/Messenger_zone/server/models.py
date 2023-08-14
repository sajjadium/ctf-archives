import tornado.escape
import tornado.ioloop
import tornado.web
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db import Base, session


def x_y_to_string(t):
    return str(t[0]) + ';' + str(t[1])

def string_to_x_y(string):
    data = string.split(';')
    return (int(data[0]), int(data[1]))


Base = declarative_base()

engine = create_engine("sqlite:///./messages.db")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    IK = Column(String)
    PK = Column(String)
    sig = Column(String)
    OPK = Column(String)

    def __init__(self, name, IK, PK, sig, OPK=None):
        self.name = name
        self.IK = IK
        self.PK = PK
        self.sig = sig
        self.OPK = OPK

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    from_m = Column(String)
    to_m = Column(String)
    header = Column(String)
    message = Column(String)

    def __init__(self, from_m, to_m, header, message):
        self.from_m = from_m
        self.to_m = to_m
        self.header = header
        self.message = message

class Keys(Base):
    __tablename__ = 'keys'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    IK = Column(String)
    EK = Column(String)
    TO = Column(String)
    MSG = Column(String)

    def __init__(self, name, IK, EK, TO, MSG):
        self.name = name
        self.IK = IK
        self.EK = EK
        self.TO = TO
        self.MSG = MSG
        
    

class RegistrationHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        # delete old data
        session.query(User).filter(User.name == data['name']).delete()

        user = User(data['name'], data['IK'], data['PK'], data['sig'], data.get('OPK'))
        session.add(user)
        session.commit()

        self.set_status(201)
        self.write({'message':'User registration'})


class SendMessageHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        message = Message(data['from_m'], data['to_m'], data['header'], data['message'])
        
        session.add(message)
        session.commit()

        self.set_status(201)
        self.write({'message':'Save msg on server'})


class GetMessageHandler(tornado.web.RequestHandler):
    def get(self):
        to_m=self.get_argument("to_m", None, True)
        msgs = session.query(Message).filter(Message.to_m == to_m).order_by(Message.id.asc()).all()
        if msgs is None:
            msgs = []
        data = []
        for msg in msgs:
            data.append({
                'id': msg.id,
                'from_m': msg.from_m,
                'to_m': msg.to_m,
                'header': msg.header,
                'message': msg.message
            })

        # delete recieved msgs
        session.query(Message).filter(Message.to_m == to_m).delete()
        session.commit()

        self.set_status(200)
        self.write({'messages': data})

class GetPublicValuesHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", None, True)
        usr = session.query(User).filter(User.name == name).first()
        if usr is None:
            self.set_status(404)
            self.write({'messages': 'No such user'})
        else:
            self.set_status(200)
            self.write({'IK':usr.IK, 'PK': usr.PK, 'sig':usr.sig, 'OPK':usr.OPK})


class KeyExchangeHandler(tornado.web.RequestHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)

        keys = session.query(Keys).filter(Keys.TO == data['to']).filter(Keys.name == data['name']).delete()
    
        keys = Keys(data['name'], x_y_to_string(data['ik']), x_y_to_string(data['ek']), data['to'], data['msg'])
        session.add(keys)
        session.commit()

        self.set_status(201)
        self.write({'message':'Init chat'})

class GeKeysHandler(tornado.web.RequestHandler):
    def get(self):
        name = self.get_argument("name", None, True)
        keys = session.query(Keys).filter(Keys.TO == name).all()
        if keys is None:
            keys = []
        data = []
        for key in keys:
            data.append([key.name, string_to_x_y(key.IK), string_to_x_y(key.EK), key.TO, key.MSG])
        self.set_status(200)
        self.write({'keys':data})




Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
