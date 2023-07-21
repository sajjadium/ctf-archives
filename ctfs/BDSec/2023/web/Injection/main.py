from flask import Flask, request , render_template
import textwrap
import sqlite3
import os
import hashlib
os.environ['FLAG'] ='test{flag}'

app = Flask(__name__)


@app.route('/login', methods=['POST' , 'GET'])
def root_data():
    data = request.form

    if 'username' not in data or 'password' not in data:
        error = 'Please Enter Both username and password'
        return render_template('index.html' , error = error)

    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    cur.execute('CREATE TABLE users (username TEXT, password TEXT)')
    cur.execute(
        'INSERT INTO users VALUES ("admin", ?)',
        [hashlib.md5(os.environ['FLAG'].encode()).hexdigest()]
    )
    output = cur.execute(
        'SELECT * FROM users WHERE username = {data[username]!r} AND password = {data[password]!r}'
        .format(data=data)
    ).fetchone()

    if output is None:
        error = "Ups! Wrong Creds!"
        return render_template('index.html' , error = error)

    username, password = output
    if username != data["username"] or password != data["password"]:
        error = 'You cant Hack Uss!!!'
        return render_template('index.html' , error = error)

    return f'Yooo!! {data["username"]}!'.format(data=data)


@app.route('/', methods=['GET'])
def root_get():
    return render_template('index.html')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7777 , debug=False)