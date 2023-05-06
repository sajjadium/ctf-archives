from flask import Flask, render_template, request
#from flask_limiter import Limiter
#from flask_limiter.util import get_remote_address

from .secret import host, user, passwd, dbname

import mysql.connector


dbconfig = {
	"host":host,
	"user":user,
	"passwd":passwd,
	"database":dbname
}

app = Flask(__name__)
"""
limiter = Limiter(
	app,
	key_func=get_remote_address,
	default_limits=["1 per second"],
)"""


#@limiter.exempt
@app.route("/")
def index():
	return render_template("index.html")


@app.route("/login")
def login():
	u = request.headers.get("User-Agent")

	conn = mysql.connector.connect(
					**dbconfig
					)

	cursor = conn.cursor()

	#cursor.execute("SET GLOBAL connect_timeout=1")
	#cursor.execute("SET GLOVAL wait_timeout=1")	
	#cursor.execute("SET GLOBAL interactive_timeout=1")

	for r in cursor.execute("SELECT * FROM Agents WHERE UA='%s'"%(u), multi=True):
		if r.with_rows:
			res = r.fetchall()
			break

	cursor.close()
	conn.close()

	

	if len(res) == 0:
		return render_template("login.html", msg="stop! you're not allowed in here >:)")

	if len(res) > 1:
		return render_template("login.html", msg="hey! close, but no bananananananananana!!!! (there are many secret agents of course)")


	return render_template("login.html", msg="Welcome, %s"%(res[0][0]))

if __name__ == '__main__':
	app.run('0.0.0.0')
