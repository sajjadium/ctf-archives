import sqlite3
import uuid
from logzero import logger
import hashlib

# make sure we have a secret for the app
try:
    SECRET = open('/tmp/secret', 'rb').read()
    logger.info(f'found secret file: {SECRET}')
except FileNotFoundError:
    SECRET = uuid.uuid4().bytes
    with open('/tmp/secret', 'wb') as f:
        f.write(SECRET)


# init database
db = sqlite3.connect('sqlite.db')

with open('schema.sql', 'r') as f:
    db.cursor().executescript(f.read())
    db.commit()

