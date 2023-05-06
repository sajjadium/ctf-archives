from sqlalchemy import Column, Boolean, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from database import Base

question_voter = Table(
    'question_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('question_id', Integer, ForeignKey('question.id'), primary_key=True)
)

answer_voter = Table(
    'answer_voter',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('answer_id', Integer, ForeignKey('answer.id'), primary_key=True)
)

### for <jump to fastapi>
class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    subject = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', backref='question_users')
    voters = relationship('User', secondary=question_voter, backref='voted_questions')
    is_markdown = Column(Boolean, nullable=True)

class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    modify_date = Column(DateTime, nullable=True)
    question_id = Column(Integer, ForeignKey("question.id"))
    question = relationship("Question", backref=backref("answers", cascade="all,delete"))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = relationship('User', backref='answer_users')
    voters = relationship('User', secondary=answer_voter, backref='voted_answers')
    is_markdown = Column(Boolean, nullable=True)

### for catgle ###
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    uploaded_model = Column(Boolean, nullable=False)
    registered_ip = Column(String(16), unique=True, nullable=False)
    last_activity = Column(DateTime, nullable=True)
    participated = Column(Integer, nullable=True)
    ranking = Column(Integer, nullable=True)
    register_date = Column(DateTime, nullable=True)

class Chall(Base):
    __tablename__ = 'chall'

    id = Column(Integer, primary_key=True)
    source = Column(Text, nullable=False)
    file_name = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='challs')
    category = Column(String(16), nullable=False)
    submission_date = Column(DateTime, nullable=True)
    failed = Column(Boolean, nullable=True)
    reason = Column(String(64), nullable=True) # reason for fail
