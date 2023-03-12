import secrets
import string
import hashlib
import sqlite3
import os

email = "johnfound@hxp.io"

username = os.getenv("ADMIN_USERNAME", "hxp_admin")
password = os.getenv("ADMIN_PASSWORD", "testtesttesttest")

if password == None or len(password) < 16:
    print(f"Admin password is somehow invalid. Password: {password}")
    print("Please run docker with sufficiently long password")
    exit(1)

if username == None or len(username) < 5:
    print(f"Admin username is somehow invalid. Username: {username}")
    exit(1)

# copied from https://stackoverflow.com/questions/3854692/generate-password-in-python
alphabet = string.ascii_letters + string.digits
salt     = ''.join(secrets.choice(alphabet) for i in range(32))

digest = hashlib.md5((salt + password).encode("ascii")).hexdigest()

# Pre-register admin
stmt = "insert into Users ( nick, passHash, salt, status, email ) values ( ?, ?, ?, -1, ?)"
connection = sqlite3.connect("./asmbb-challenge/board.sqlite")
cursor = connection.cursor()
res = cursor.execute(stmt, (username, digest, salt, email))

# Remove confirmation need
stmt = "update Params SET val='0' where id='email_confirm'"
res = cursor.execute(stmt)

connection.commit()
