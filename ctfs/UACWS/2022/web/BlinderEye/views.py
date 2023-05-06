from flask import request, send_from_directory, render_template
from app import app
import sqlite3
import hashlib

def checkSecret(_username, _password):
    # check user exists			
    # connection object
    connection_obj = sqlite3.connect('/challenge/app/data/blindereye.db')
  
    # cursor object
    cursor_obj = connection_obj.cursor()
    
    cursor_obj.execute(f"SELECT * FROM USERS WHERE username = '{_username}' AND password = '{_password}'")
    result = cursor_obj.fetchone()

    if result:
        return True
    else:
        return False

@app.route('/', methods=['GET'])
def home():
	return render_template('home.html')

# robots.txt file
@app.route('/robots.txt', methods=['GET'])
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/admin', methods=['GET'])
def admin():
    args = request.args
    _username = args.get('username')
    _password = args.get('password')

    # validate secrets
    if _username and _password and checkSecret(_username, _password):
        return render_template('admin.html')
    else:
        return render_template('404.html'), 404

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404