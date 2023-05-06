import sqlite3
from uuid import uuid4
from pathlib import Path

path = Path(__file__).resolve().parent / 'database/db.sqlite3'

def conn_db():
    conn = sqlite3.connect(path, check_same_thread=False)
    cur = conn.cursor()
    return (conn, cur)


if __name__ == '__main__':

    path.parent.mkdir(parents=True, exist_ok=True)
    conn, cur = conn_db()

    cur.executescript('''
        DROP TABLE IF EXISTS posts;
        CREATE TABLE posts (id BLOB PRIMARY KEY, title TEXT, content TEXT, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
    ''')

    uuid = lambda: str(uuid4())
    posts = [
        (uuid(), 'fleece fleece fleece', 'i love wearing fleece-colored jackets. they are very soft.'),
        (uuid(), 'e - the best letter in the alphabet', 'fleece is made of 50 percent e\'s. it also precedes the letter f, which is what fleece starts with. that is why it is the best letter in the alphabet.'),
        (uuid(), 'fleece use', 'while sometimes used for fashion, fleece is often used for comfort. hug some fleece today and learn about your fleece aspirations.'),
        (uuid(), 'mary fleece hoax', 'contrary to popular belief, mary did not befriend a lamb with fleece. either way, the lamb died.'),
        (uuid(), 'cool facts about the word fleece', 'did you know that there are 120 distinct ways to re-arrange the letters in fleece? fleece also has no 6-letter anagrams.'),
    ]
    cur.executemany('INSERT INTO posts (id, title, content) VALUES (?, ?, ?);', posts)

    conn.commit()
    conn.close()
