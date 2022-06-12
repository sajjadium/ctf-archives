import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'yolo-that-would-be-too-easy'*2)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:////tmp/app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
