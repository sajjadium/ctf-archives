from flask import Flask,request,render_template,session,redirect
from flask_wtf.csrf import CSRFProtect
from form import ReportForm
import os,ipaddress,pymysql
import requests

app= Flask(__name__)
app.config["SECRET_KEY"]=os.urandom(15).hex()
app.config['RECAPTCHA_USE_SSL']= False
app.config['RECAPTCHA_PUBLIC_KEY']= os.getenv("PUBLIC_KEY")
app.config['RECAPTCHA_PRIVATE_KEY']=os.getenv("PRIVATE_KEY")
app.config['RECAPTCHA_OPTIONS'] = {'theme':'white'}
flag=os.getenv("FLAG")
mydb = pymysql.connect(
  host="db",
  user="fword",
  password=os.getenv("mysql_pass"),
  database="task"
)
csrf=CSRFProtect()
csrf.init_app(app)


def get_db():
    return mydb.cursor()


@app.route("/",methods=["GET"])
def index():
	return render_template("index.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        if "username" in session :
            return redirect("/home")
        if request.values.get("username") and len(request.values.get("username"))<50 and request.values.get("password"):
            cursor = get_db()
            query = "SELECT * FROM users WHERE username=%s"
            cursor.execute(query, request.values.get("username"))
            result = cursor.fetchone()
            if result is not None:
                return render_template("register.html",error="Username already exists")
            try:
                mydb.commit()
                cursor.close()
                cursor=get_db()
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
        return render_template("home.html",username=session["username"])
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
            cursor = get_db()
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

@app.route("/flag",methods=["GET"])
def flagEndpoint():
	if "username" in session:
		ip=request.remote_addr
		an_address = ipaddress.ip_address(ip)
		a_network = ipaddress.ip_network('172.16.0.0/24')
		if(an_address in a_network):
			return flag
		else:
			return "Damn Hackers Nowadays"
	else:
		return redirect("/login")


# No vulns here just the bot implementation
@app.route("/report",methods=["POST","GET"])
def report():
	form= ReportForm()
	if request.method=="POST":
		if form.validate_on_submit():
			r=requests.get("http://bot?url="+request.form.get("url"))
			if "successfully" in r.text:
				return render_template("report.html",form=form,msg="Admin visited your website successfully")
			else:
				return render_template("report.html",form=form,msg="An unknown error has occured")
	else:
		return render_template("report.html",msg="",form=form)


if __name__=="__main__":
	app.run(host="0.0.0.0",debug=False)
