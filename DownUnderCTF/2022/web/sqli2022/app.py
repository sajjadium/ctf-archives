from flask import Flask, request
import textwrap
import sqlite3
import os
import hashlib

assert len(os.environ['FLAG']) > 32

app = Flask(__name__)

@app.route('/', methods=['POST'])
def root_post():
    post = request.form
    
    # Sent params?
    if 'username' not in post or 'password' not in post:
        return 'Username or password missing from request'

    # We are recreating this every request
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute('CREATE TABLE users (username TEXT, password TEXT)')
    cur.execute(
        'INSERT INTO users VALUES ("admin", ?)',
        [hashlib.md5(os.environ['FLAG'].encode()).hexdigest()]
    )
    output = cur.execute(
        'SELECT * FROM users WHERE username = {post[username]!r} AND password = {post[password]!r}'
        .format(post=post)
    ).fetchone()
    
    # Credentials OK?
    if output is None:
        return 'Wrong credentials'
    
    # Nothing suspicious?
    username, password = output
    if username != post["username"] or password != post["password"]:
        return 'Wrong credentials (are we being hacked?)'
    
    # Everything is all good
    return f'Welcome back {post["username"]}! The flag is in FLAG.'.format(post=post)

@app.route('/', methods=['GET'])
def root_get():
    return textwrap.dedent('''
       <html>
         <head></head>
         <body>
           <form action="/" method="post">
             <p>Welcome to admin panel!</p>
             <label for="username">Username:</label>
             <input type="text" id="username" name="username"><br><br>
             <label for="password">Password:</label>
             <input type="text" id="password" name="password"><br><br>
             <input type="submit" value="Submit">
          </form> 
         </body>
       </html>
    ''').strip()