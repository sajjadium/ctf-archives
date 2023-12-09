import os
from db import db

cursor = db.cursor()
cursor.execute("SELECT secret from secret")
firstSecret = cursor.fetchone()[0]
secondSecret = os.getenv('SECRET', 'TEST_SECRET')
secret = secondSecret + firstSecret
flag = os.getenv('FLAG', 'ping{FAKE}')
