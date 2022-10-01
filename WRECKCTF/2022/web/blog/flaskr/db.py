import sqlite3

from werkzeug.security import generate_password_hash

db = sqlite3.connect(
    'data/db.sqlite3',
    detect_types=sqlite3.PARSE_DECLTYPES,
    isolation_level=None,
)
db.row_factory = sqlite3.Row

def get_db():
    return db

SCHEMA = '''
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);
'''

def init_db():
    db.executescript(SCHEMA)

    username = "GeorgePBurdell"

    try:
        res = db.execute(
            "INSERT INTO user (username, password) VALUES (?, ?)",
            (username, generate_password_hash(open("flaskr/protected/burdellsecrets.txt").read())),
        )
    except sqlite3.IntegrityError:
        return

    db.execute(
        'INSERT INTO post (title, body, author_id)'
        ' VALUES (?, ?, ?)',
        ("No one can read my secrets :)", "/flaskr/protected/burdellsecrets.txt", res.lastrowid)
    )
    db.commit()
