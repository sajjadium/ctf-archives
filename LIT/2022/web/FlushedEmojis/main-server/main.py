import sqlite3
from flask import Flask, render_template, render_template_string, redirect, url_for, request
import requests;
import re;

app = Flask(__name__)


def alphanumericalOnly(str):
  return re.sub(r'[^a-zA-Z0-9]', '', str);

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':

    username = request.form['username']
    password = request.form['password']

  
    if('.' in password):
      return render_template_string("lmao no way you have . in your password LOL");

    r = requests.post('[Other server IP]', json={"username": alphanumericalOnly(username),"password": alphanumericalOnly(password)}); 
    print(r.text);
    if(r.text == "True"):
      return render_template_string("OMG you are like so good at guessing our flag I am lowkey jealoussss.");
    return render_template_string("ok thank you for your info i have now sold your password (" + password + ") for 2 donuts :)");

  return render_template("index.html");


app.run(host='127.0.0.1',port=8081,debug=True)