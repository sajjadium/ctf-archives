import random
import string
from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

con = sqlite3.connect('database.db')

sessions = []

with sqlite3.connect('database.db') as con:
  cursor = con.cursor()
  cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, sus BOOLEAN)')

@app.route('/', methods=['GET'])
def index():
  return jsonify({'message': 'Welcome to the amogsus API! I\'ve been working super hard on it in the past few weeks. You can use a tool like postman to test it out. Start by signing up at /signup. Also, I think I might have forgotten to sanatize an input somewhere... Good luck!'})


@app.route('/signup', methods=['POST'])
def signup():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    data = request.form
    print(data)
    username = data['username']
    password = data['password']
    sus = False
    cursor.execute('SELECT * FROM users WHERE username=?', (username,))
    if cursor.fetchone():
      return jsonify({'message': 'Username already exists!'})
    else:
      cursor.execute('INSERT INTO users (username, password, sus) VALUES (?, ?, ?)', (username, password, sus))
      con.commit()
      return jsonify({'message': 'User created! You can now login at /login'})

@app.route('/login', methods=['POST'])
def login():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    data = request.form
    try:
      username = data['username']
      password = data['password']
      cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
      user = cursor.fetchone()
      if user:
        randomToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        while randomToken in sessions:
          randomToken = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))
        sessions.append({'username': username, 'token': randomToken})
        return jsonify({'message': 'Login successful! You can find your account information at /account. Make sure to provide your token! You should know how to bear your Authorization...', 'token': randomToken})
      else:
        return jsonify({'message': 'Login failed!'})
    except Exception as e:
      print(e)
      return jsonify({'message': 'Please provide your username and password as form-data or x-www-form-urlencoded!'})
    

@app.route('/account', methods=['GET'])
def account():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          cursor.execute('SELECT * FROM users WHERE username=?', (session['username'],))
          user = cursor.fetchone()
          return jsonify({'message': 'Here is your account information! You can update your account at /account/update. The flag can also be found at /flag. You need to be sus to get access tho...', 'username': user[1], 'sus': user[3], "password": user[2]})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})
    
@app.route('/account/update', methods=['POST'])
def update():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          data = request.form
          username = data['username']
          password = data['password']
          if (username == '' or password == ''):
            return jsonify({'message': 'Please provide your new username and password as form-data or x-www-form-urlencoded!'})
          cursor.execute(f'UPDATE users SET username="{username}", password="{password}" WHERE username="{session["username"]}"')
          con.commit()
          session['username'] = username
          return jsonify({'message': 'Account updated!'})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})

@app.route('/flag', methods=['GET'])
def flag():
  with sqlite3.connect('database.db') as con:
    cursor = con.cursor()
    token = request.headers.get('Authorization', type=str)
    token = token.replace('Bearer ', '')
    if token:
      for session in sessions:
        if session['token'] == token:
          cursor.execute('SELECT * FROM users WHERE username=?', (session['username'],))
          user = cursor.fetchone()
          if user[3]:
            return jsonify({'message': f'Congrats! The flag is: flag{open("./flag.txt", "r").read()}'})
          else:
            return jsonify({'message': 'You need to be an sus to view the flag!'})
      return jsonify({'message': 'Invalid token!'})
    else:
      return jsonify({'message': 'Please provide your token!'})
    

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8080)