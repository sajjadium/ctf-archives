from flask import Flask,request,render_template,session,redirect
from form import ReportForm,LoginForm,RegisterForm
import os,pymysql,time
import requests,secrets,random,string
from flask_wtf.csrf import CSRFProtect

app= Flask(__name__)
app.config["SECRET_KEY"]=os.urandom(15).hex()
app.config['RECAPTCHA_USE_SSL']= False
DOMAIN=os.getenv("DOMAIN")
app.config['RECAPTCHA_PUBLIC_KEY']= os.getenv("PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY']=os.getenv("PRIVATE_KEY")
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
app.config['SESSION_COOKIE_SAMESITE']="None"
app.config['SESSION_COOKIE_SECURE']= True

csrf = CSRFProtect()
csrf.init_app(app)

def random_string(S):
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    return ran

def get_db():
    mydb = pymysql.connect(
    host="db",
    user="securinets",
    password=os.getenv("mysql_pass"),
    database="l33k"
    )
    return mydb.cursor(),mydb


def create_paste(paste, username):
    paste_id = random_string(64)
    cursor,mydb=get_db()
    cursor.execute(
    'INSERT INTO pastes (id, paste, username) VALUES (%s, %s, %s);',
    (paste_id, paste, username)
    )
    mydb.commit()
    return paste_id


def get_pastes(username):
    cursor,mydb=get_db()
    cursor.execute(
    'SELECT id FROM pastes WHERE username = %s',
    username
    )
    result=cursor.fetchall()
    mydb.commit()
    return [paste_id[0] for paste_id in result]

def get_paste(paste_id):
    cursor,mydb=get_db()
    cursor.execute(
    'SELECT paste FROM pastes WHERE id = %s',
    paste_id
    )
    results=cursor.fetchone()
    mydb.commit()
    if len(results) < 1:
        return 'Paste not found!'
    return results[0]


@app.route("/",methods=["GET"])
def index():
	return render_template("index.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        if "username" in session :
            return redirect("/home")
        if request.values.get("username") and len(request.values.get("username"))<50 and request.values.get("password"):
            cursor,mydb = get_db()
            query = "SELECT * FROM users WHERE username=%s"
            cursor.execute(query, request.values.get("username"))
            result = cursor.fetchone()
            if result is not None:
                return render_template("register.html",error="Username already exists")
            try:
                mydb.commit()
                cursor.close()
                cursor,mydb=get_db()
                query="INSERT INTO users(id,username,password) VALUES(null,%s,%s)"
                values=(request.values.get("username"),request.values.get("password"))
                cursor.execute(query,values)
                mydb.commit()
                session["username"]=request.values.get("username")
                cursor.close()
                return redirect("/home")
            except Exception:
                return render_template("register.html",error="Error happened while registering")
        else:
            return redirect("/login",302)
    else:
        if "username" in session:
            return redirect("/home")
        else:
            return render_template("register.html",error="")



@app.route("/home",methods=["GET"])
def home():
    if "username" in session :
       print(get_pastes(session['username']))
       return render_template("home.html",username=session["username"],pastes=get_pastes(session['username']))
    else:
        return redirect("/login")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        if "username" in session:
            return redirect("/home")
        else:
            return render_template("login.html",error="")
    else:
        username=request.values.get("username")
        password=request.values.get("password")
        if username is None or password is None:
            return render_template("login.html",error="")
        else:
            cursor,mydb = get_db()
            query = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result is not None:
                session["username"]=result[1]
                mydb.commit()
                cursor.close()
                return redirect("/home")
            else:
                return render_template("login.html",error="Username or password is incorrect")

@app.route("/logout",methods=["GET"])
def logout():
	session.clear()
	return redirect("/")

@app.route('/source',methods=['GET'])
def source():
	return render_template("source.html")



@app.route('/create_paste', methods=['POST','GET'])
def create():
    if request.method=="GET":
        if 'username' not in session:
            return redirect('/login')
        return render_template("create_paste.html")
    else:
        if 'username' not in session:
            return redirect('/login')
        if len(request.values.get('paste'))<1000:
            paste_id = create_paste(
                request.values.get('paste'),
                session['username']
            )
            return redirect('/view?id='+paste_id)
        return redirect('/home')

@app.route('/view', methods=['GET'])
def view():
    paste_id = request.args.get('id')
    if paste_id=="MaximumReached" :
        return render_template("view.jinja2",paste="Maximum iterations is reached! your last paste is: "+request.args.get("paste"))
    if paste_id=="Found":
        return render_template("view.jinja2",paste="Found your search!. your last paste is: "+request.args.get("paste"))
    return render_template(
        'view.jinja2',
        paste=get_paste(paste_id)
    )


@app.route('/search')
def search():
    if 'username' not in session:
        return redirect('/login')
    if 'query' not in request.args:
        return redirect('/home')
    query = str(request.args.get('query'))
    results = get_pastes(session['username'])
    res_content=[{"id":id,"val":get_paste(id)} for id in results]
    if ":" in query:
        toGo=get_paste(query.split(":")[1])
        sear=query.split(":")[0]
    else:
        toGo=res_content[0]["val"]
        sear=query
    i=0
    for paste in res_content:
        i=i+1
        if i>5:
            return redirect("/view?id=MaximumReached&paste="+toGo.strip())     
        if sear in paste["val"]:
            return redirect("/view?id=Found&paste="+toGo.strip())
    return render_template("search.html",error='No results found.',result="")

# No vulns here just the bot implementation
@app.route("/report",methods=["POST","GET"])
def report():
	form= ReportForm()
	if request.method=="POST":
		r=requests.get("http://bot?url="+request.form.get("url"))
		if "successfully" in r.text:
			return render_template("report.html",form=form,msg="Admin visited your website successfully")
		else:
			return render_template("report.html",form=form,msg="An unknown error has occured")
	else:
		return render_template("report.html",msg="",form=form)


if __name__=="__main__":
	app.run(host="0.0.0.0",debug=False,port=443,ssl_context='adhoc')

