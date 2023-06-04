from flask import Flask, render_template, session
import os
app = Flask(__name__)
SECRET_KEY = os.urandom(2)
app.config['SECRET_KEY'] = SECRET_KEY
FLAG = open("flag.txt", "r").read()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/flag')
def get_flag():
    if "name" not in session:
        session['name'] = "user"
    is_admin = session['name'] == "admin"
    return render_template("flag.html", flag=FLAG, admin = is_admin)

if __name__ == '__main__':
    app.run()