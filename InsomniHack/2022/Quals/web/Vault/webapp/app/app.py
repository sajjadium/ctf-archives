#!/usr/bin/python3
from flask import Flask, render_template, jsonify, request, session
from flask.sessions import SecureCookieSessionInterface
import pyodbc
from flask_session import Session
import os
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'FileSystemSessionInterface'
app.config['SESSION_FILE_DIR'] = '/tmp'
admin_conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=db,1433;"
            "Database=Vault;"
            "UID=sa;"
            "PWD=" + os.environ.get("SA_PASSWORD") + ";")
SESSION_COOKIE_HTTPONLY = True

def is_safe(s):
    pattern = re.compile("^[a-zA-Z0-9-_!]+$")
    if pattern.match(s):
        return True
    return False


@app.route('/')
def index():
    if "username" in session:
        return render_template("index.html", login="Logout")
    else:
        return render_template("index.html", login="Login")

@app.route('/api/secrets', methods=['GET','POST'])
def secrets():
    if "username" in session and "password" in session:
        if request.method == 'POST':
            conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=db,1433;"
            "Database=Vault;"
            "UID=" + session["username"] + ";"
            "PWD=" + session["password"])
            conn = pyodbc.connect(conn_str, autocommit=True)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO dbo.Vault (username,secret_name,secret_value) VALUES (?,?,?)", session["username"],request.form["secret_name"],request.form["secret_value"])
            cursor.execute("INSERT INTO dbo.Stats (username) VALUES (?)", session["username"])
            cursor.close()
            conn.close()
            return {'status':'OK'}
        else:
            conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server=db,1433;"
                "Database=Vault;"
                "UID=" + session["username"] + ";"
                "PWD=" + session["password"])
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            sql = "SELECT secret_name,secret_value FROM dbo.Vault ;"
            cursor.execute(sql)
            res = cursor.fetchall()
            ret = []
            for row in res:
                ret.append({'secret_name':row[0], 'secret_value':row[1]})
            cursor.close()
            conn.close()
            return {'status':'OK','result':ret}
    else:
        return {'status': 'KO','msg':'Not logged in!'}

@app.route('/api/register', methods=['POST'])
def register():
    credentials = request.form
    if is_safe(credentials["username"]) and is_safe(credentials["password"]):
        try:
            conn = pyodbc.connect(admin_conn_str, autocommit=True)
            cursor = conn.cursor()
            sql = "EXEC dbo.CreateUser @login=?,@password=?"
            cursor.execute(sql,credentials["username"],credentials["password"])
            cursor.close()
            conn.close()
            return {'status':'OK'}
        except:
            return {'status':'KO','msg':'Registration error'}
    else:
        return {'status':'KO','msg':'Invalid user or pwd'}

@app.route('/api/login', methods=['POST'])
def login():
    credentials = request.form
    if is_safe(credentials["username"]) and is_safe(credentials["password"]):
        try:   
            conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=db,1433;"
            "Database=Vault;"
            "UID="+credentials["username"] +";"
            "PWD="+credentials["password"]+";")
            conn = pyodbc.connect(conn_str, autocommit=True)
            session["username"] = credentials["username"]
            session["password"] = credentials["password"]
            if credentials["username"] == "admin":
                session["admin"] = 1;
            return {'status':'OK'}
        except:
            return {'status':'KO','msg':'Login failed'}
    else:
        return {'status':'KO','msg':'Invalid user or pwd'}
    

@app.route('/api/logout')
def logout():
    del session["username"]
    del session["password"]
    return {'status':'OK'}

@app.route('/api/stats')
def stats():
    if not "admin" in session or session["admin"] != 1:
        return {'status':'KO', 'msg': 'You are not admin'}
    else:
        try:
            conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
                "Server=db,1433;"
                "Database=Vault;"
                "UID=" + session["username"] + ";"
                "PWD=" + session["password"])
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            sql = "SELECT inserttime FROM dbo.Stats WHERE username = '" + request.args.get("username") + "'"
            cursor.execute(sql)
            res=cursor.fetchall()
            ret=[]
            for row in res:
                ret.append({'inserttime':row[0]})
            cursor.close()
            conn.close()
            return {'status':'OK','results':ret}
        except:
            return {'status':'NOK'}


@app.route('/api/report', methods=['POST'])
def contact():
    url = request.form["url"]
    pattern = re.compile("^https?:\/\/")
    if len(url) > 0 and pattern.match(url):
        try:
            from selenium import webdriver  
            from selenium.webdriver.common.keys import Keys  
            from selenium.webdriver.chrome.options import Options 
            import time
            session_serializer = SecureCookieSessionInterface().get_signing_serializer(app)
            adminsession = dict()
            adminsession["admin"] = 1
            adminsession["username"] = "admin"
            adminsession["password"] = os.environ.get("ADMIN_PWD")
            session_cookie = session_serializer.dumps(dict(adminsession))
            chrome_options = Options()  
            chrome_options.headless = True
            chrome_options.add_argument('--no-sandbox')
            driver = webdriver.Chrome("/app/chromedriver", options=chrome_options)  
            driver.set_page_load_timeout(30)
            driver.get("http://" + os.environ.get("VHOST") + "/")
            time.sleep(1)
            driver.add_cookie({"name": "session", "value":session_cookie,"httpOnly": True})
            driver.get(url)
            time.sleep(30)
            driver.close()
            return {'status':'OK'}
        except:
            return {'status':'KO','msg':'Error checking page'}
    return {'status':'KO','msg':'Invalid URL'}


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    