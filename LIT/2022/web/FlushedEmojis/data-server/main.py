import sqlite3
from flask import Flask, render_template, render_template_string, redirect, url_for, request

con = sqlite3.connect('data.db', check_same_thread=False)
app = Flask(__name__)

flag = open("flag.txt").read();

cur = con.cursor()

cur.execute('''DROP TABLE IF EXISTS users''')
cur.execute('''CREATE TABLE users (username text, password text)''')
cur.execute(
    '''INSERT INTO users (username,password) VALUES ("flag","''' + flag + '''") '''
)


@app.route('/runquery', methods=['POST'])
def runquery():
  request_data = request.get_json()
  username = request_data["username"];
  password = request_data["password"];

  print(password);
  
  cur.execute("SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'");

  rows = cur.fetchall()
  if(len(rows) > 0):
    return "True";
  return "False";

app.run(host='127.0.0.1',port=8080,debug=True)
