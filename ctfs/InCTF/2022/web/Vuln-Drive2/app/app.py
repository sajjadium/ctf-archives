from lib2to3.pgen2 import token
import re
from flask import Flask,request
app = Flask(__name__)
import sqlite3
import os
FLAG = os.environ.get('FLAG',"flag{fakeflag}")


def db_query(query):
    conn = sqlite3.connect(os.path.join(os.path.realpath(os.curdir),'users.db'))
    cursor = conn.cursor()
    result = cursor.execute(query)
    conn.commit()
    return result


def init_db():
    try: 
        conn = sqlite3.connect(os.path.join(os.path.realpath(os.curdir),'users.db'))
        cursor = conn.cursor()
        result = cursor.executescript(f"""
            CREATE TABLE IF NOT EXISTS users  (
                                                    username  TEXT, 
                                                    token TEXT
                                                );
            CREATE TABLE IF NOT EXISTS flag  (
                                                flag_is_here  TEXT
                                            );                                                  
            Delete from users;
            Delete from flag;
            INSERT INTO users values ('user','some_randomtoken'),
                                    ('admi','some_randomtoken'),
                                    (
                                        'admin',
                                        '{FLAG}'
                                    );
            INSERT INTO flag values ('{FLAG}');
            """)
        conn.commit()
        return True
    except:
        return False

   
def add_user(user,token):
    q = f"INSERT INTO users values ('{user}','{token}')"
    db_query(q)
    return

@app.route("/")
def index():
    while not init_db():
        continue
    if request.headers.get("X-pro-hacker")=="Pro-hacker" and "gimme" in request.headers.get("flag"):
        try:
            if request.headers.get("Token"):         
                token = request.headers.get("Token")
                token = token[:16]
                token = token.replace(" ","").replace('"',"")
                if request.form.get("user"):
                    user = request.form.get("user")
                    user = user[:38]
                    add_user(user,token)            
                query = f'SELECT * FROM users WHERE token="{token}"'
                res = db_query(query)
                res = res.fetchone()
                return res[1] if res and len(res[0])>0  else "INDEX\n"
        except Exception as e:
            print(e) 
    return "INDEX\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
