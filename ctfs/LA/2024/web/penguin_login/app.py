import string
import os
from functools import cache
from pathlib import Path

import psycopg2
from flask import Flask, request

app = Flask(__name__)
flag = Path("/app/flag.txt").read_text().strip()

allowed_chars = set(string.ascii_letters + string.digits + " 'flag{a_word}'")
forbidden_strs = ["like"]


@cache
def get_database_connection():
    # Get database credentials from environment variables
    db_user = os.environ.get("POSTGRES_USER")
    db_password = os.environ.get("POSTGRES_PASSWORD")
    db_host = "db"

    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(user=db_user, password=db_password, host=db_host)

    return connection


with app.app_context():
    conn = get_database_connection()
    create_sql = """
        DROP TABLE IF EXISTS penguins;
        CREATE TABLE IF NOT EXISTS penguins (
            name TEXT
        )
    """
    with conn.cursor() as curr:
        curr.execute(create_sql)
        curr.execute("SELECT COUNT(*) FROM penguins")
        if curr.fetchall()[0][0] == 0:
            curr.execute("INSERT INTO penguins (name) VALUES ('peng')")
            curr.execute("INSERT INTO penguins (name) VALUES ('emperor')")
            curr.execute("INSERT INTO penguins (name) VALUES ('%s')" % (flag))
        conn.commit()


@app.post("/submit")
def submit_form():
    try:
        username = request.form["username"]
        conn = get_database_connection()

        assert all(c in allowed_chars for c in username), "no character for u uwu"
        assert all(
            forbidden not in username.lower() for forbidden in forbidden_strs
        ), "no word for u uwu"

        with conn.cursor() as curr:
            curr.execute("SELECT * FROM penguins WHERE name = '%s'" % username)
            result = curr.fetchall()

        if len(result):
            return "We found a penguin!!!!!", 200
        return "No penguins sadg", 201

    except Exception as e:
        return f"Error: {str(e)}", 400

    # need to commit to avoid connection going bad in case of error
    finally:
        conn.commit()


@app.get("/")
def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Penguin Login</title>
</head>
<body style="background-image: url(https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F1.bp.blogspot.com%2F-XVeENb41J0o%2FU8pY9kr6peI%2FAAAAAAAAM7Y%2F2h28ZEQ7mKs%2Fs1600%2F3.%2BThis%2Bshuffle.%2B-%2B17%2BTimes%2BBaby%2BPenguins%2BReached%2BDangerous%2BLevels%2BOf%2BCuteness.%2BBe%2BAfraid..gif&f=1&nofb=1&ipt=4800f83a172449a4f6d683d33bd7a208d29d214e4dee637302947dff1508e5bc&ipo=images)">
    <form action="/submit" method="POST">
        <input type="text" name="username" style="width: 80vw">
    </form>
</body>
</html>
""", 200

if __name__ == "__main__":
    app.run(debug=True)
