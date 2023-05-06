from flask import Flask, render_template, request
from random import choice
import sqlite3
from sqlite3 import Error

web_site = Flask(__name__)

@web_site.route('/')
def index():
    return render_template('index.html')

@web_site.route('/user')
def user():
  try:
    username = request.args.get('username')
    password = request.args.get('password')
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    resp = c.fetchone()
    if resp != None:
      return "Welcome, admin. You logged in. The flag is not ictf{fake_flag}."
    else:
      return "You didn't log in. Sad."
  except:
    return "You didn't log in. Sad."

web_site.run(host='0.0.0.0', port=6969)