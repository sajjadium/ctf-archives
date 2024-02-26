from flask import Flask,render_template,request,session,redirect,Response
from flask_caching import Cache
import sqlite3
import os
from urllib.parse import urlsplit
import base64
import uuid


cache = Cache()
curr_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(curr_dir,"user_uploads")
app.secret_key = str(uuid.uuid4())
app.config['MAX_CONTENT_LENGTH'] = 1 * 1000 * 1000
app.config['CACHE_TYPE'] = 'FileSystemCache'
app.config['CACHE_DIR'] = './caches'
app.config['CACHE_THRESHOLD'] = 100000
cache.init_app(app)

def getDB():
    conn = sqlite3.connect(os.path.join(curr_dir,"docview.db"))
    cursor = conn.cursor()
    return cursor,conn


def isSecure(title):
    D_extns = ['py','sh']
    D_chars = ['*','?','[',']']
    extension = title.split('.')[-1]
    if(extension in D_extns):
        return False
    for char in title:
        if char in D_chars:
            return False
    return True


@app.route('/',methods=["GET"])
def index():
    return redirect("/login",code=302)

@app.route('/dashboard',methods=["GET"])
@cache.cached(timeout=1,query_string=True)
def home():
    try:
        if(session.get("loggedin") != "true"):
            return redirect('/login',code=302)
        file_path = os.path.join(UPLOAD_FOLDER,session.get('id'))
        notes_list = os.listdir(file_path)
        return render_template('dashboard.html',message=session.get('user'),notes=notes_list)
    except Exception as e:
        print(f"ERROR: {e}",flush=True)
        return "You broke the server :(",400

@app.route('/login',methods=["GET","POST"])
def login():
    try:
        if(session.get("loggedin") == "true"):
            return redirect('/dashboard',code=302)
        if(request.method == "POST"):
            user = request.form.get("username").strip()
            passw = request.form.get("password").strip()
            cursor,conn = getDB()
            rows = cursor.execute("SELECT username,docid FROM accounts WHERE username = ? and password=?",(user,passw,)).fetchone()
            if rows:
                session["loggedin"] = "true"
                session["user"] = user
                session['id'] = rows[1]
                file_path = os.path.join(UPLOAD_FOLDER,session.get('id'))
                notes_list = os.listdir(file_path)
                return render_template('dashboard.html',message=session.get("user"),notes=notes_list)
            return render_template('login.html',message="Username/Password doesn't match")
        return render_template('login.html')
    except Exception as e:
        print(f"ERROR: {e}",flush=True)
        return "You broke the server :(",400

@app.route('/register',methods=["GET","POST"])
def register():
    try:
        if(request.method == "POST"):
            user = request.form.get("username").strip()
            passw = request.form.get("password").strip()
            cursor,conn = getDB()
            rows = cursor.execute("SELECT username FROM accounts WHERE username = ?",(user,)).fetchall()
            if rows:
                return render_template('register.html',message="user already exists")
            direc_id = str(uuid.uuid4())
            query = "INSERT INTO accounts VALUES(?,?,?)"
            res = cursor.execute(query,(user,passw,direc_id))
            conn.commit()
            if(res):
                os.mkdir(os.path.join(UPLOAD_FOLDER,direc_id))
                return redirect('/login')
        return render_template('register.html')
    except Exception as e:
        print(f"ERROR: {e}",flush=True)
        return "You broke the server :(",400

@app.route('/makenote',methods=["POST"])
def upload():
    try:
        if(session.get("loggedin") != "true"):
            return redirect('/login',code=302)
        title = request.form.get('title')
        content = base64.b64decode(request.form.get('content'))
        if(title == None or title==""):
            return render_template('dashboard.html',err_msg="title cannot be empty"),402
        if(not isSecure(title)):
            return render_template('dashboard.html',err_msg="invalid title")
        file_path = os.path.join(UPLOAD_FOLDER,session.get('id'))
        notes_list = os.listdir(file_path)
        try:
            file = os.path.join(file_path,title)
            if('caches' in os.path.abspath(file)):
                return render_template('dashboard.html',err_msg="invalid title",notes = notes_list),400
            with open(file,"wb") as f:
                f.write(content)
        except Exception as e:
            print(f"ERROR: {e}",flush=True)
            return render_template('dashboard.html',err_msg="Some error occured",notes = notes_list),400
        return redirect('/dashboard',code=302)
    except Exception as e:
        print(f"ERROR: {e}",flush=True)
        return "You broke the server :(",400

@app.route('/viewnote/<title>',methods=["GET"])
def viewnote(title):
    try:
        if(session.get("loggedin") != "true"):
            return redirect('/login',code=302)
        cursor,conn = getDB()
        res = cursor.execute("SELECT docid FROM accounts WHERE username=?",(session.get('user'),)).fetchone()
        path = os.path.join(UPLOAD_FOLDER,res[0])
        notes_list = os.listdir(path)
        if(title in notes_list):
            with open(os.path.join(path,title),"rb") as f:
                return f.read()
        return "The note doesn't exist/you dont have access",400
    except Exception as e:
        print(f"ERROR: {e}",flush=True)
        return "You broke the server :(",400
    

@app.route("/logout",methods=["GET","POST"])
def logout():
    session.pop('loggedin')
    session.pop('id')
    session.pop('user')
    return redirect("/login",code=302)

if(__name__=="__main__"):
    app.run(host="0.0.0.0",port=7000,debug=False)