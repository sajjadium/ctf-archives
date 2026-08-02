import sqlite3
import sys
from os import urandom

if len(sys.argv) < 2:
    print(f"Usage: python {sys.argv[0]} <admin username>.")
    exit(1)

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

adminUsername = sys.argv[1]
adminPassword = urandom(16).hex()

cur.execute("INSERT INTO users (email, username, password, admin) VALUES (?, ?, ?, ?)",
            (f'{adminUsername}@admins.hihi1839203981.aazz', adminUsername, adminPassword, True)
            )

cur.execute("INSERT INTO comments (username, content) VALUES (?, ?)",
            (adminUsername, 'Test comment')
            )

connection.commit()
connection.close()
