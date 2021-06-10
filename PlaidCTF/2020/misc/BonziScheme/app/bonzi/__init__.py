from flask import Flask
from config import Config
from flask_uuid import FlaskUUID

app = Flask(__name__)
app.config.from_object(Config)
FlaskUUID(app)

from bonzi import routes, errors