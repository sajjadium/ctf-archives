from flask import Flask,render_template,request,session,redirect
import pymongo
import os
from functools import wraps
from datetime import timedelta
from hashlib import md5
from time import sleep

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

# db settings
client = pymongo.MongoClient('localhost',27017)
db = client.ctfdb

def createChalls():
	db.challs.insert_one({"_id": "28c8edde3d61a0411511d3b1866f0636","challenge_name": "Crack It","category": "hash","challenge_description": "My friend sent me this random string `cc4d73605e19217bf2269a08d22d8ae2` can you identify what it is? , flag format: CTFC{<password>}","challenge_flag": "CTFC{cryptocat}","points": "500","released": "True"})
	db.challs.insert_one({"_id": "665f644e43731ff9db3d341da5c827e1","challenge_name": "MeoW sixty IV","category": "crypto","challenge_description": "hello everyoneeeeeeeee Q1RGQ3tuMHdfZzBfNF90aDNfcjM0TF9mbDRHfQ==, oops sorry my cat ran into my keyboard, and typed these random characters","challenge_flag": "CTFC{n0w_g0_4_th3_r34L_fl4G}","points": "1000","released": "True"})
	db.challs.insert_one({"_id": "38026ed22fc1a91d92b5d2ef93540f20","challenge_name": "ImPAWSIBLE","category": "web","challenge_description": "well, this challenge is not fully created yet, but we have the flag for it","challenge_flag": os.environ['CHALL_FLAG'],"points": "1500","released": "False"})

# login check
def check_login(f):
	@wraps(f)
	def wrap(*args,**kwrags):
		if 'user' in session:
			return f(*args,**kwrags)
		else:
			return render_template('dashboard.html')
	return wrap

# routes
from user import routes

@app.route('/')
@check_login
def dashboard():
	challs = []
	for data in db.challs.find():
		del data['challenge_flag']
		challs.append(data)	
	chall_1 = challs[0]
	chall_2 = challs[1]
	return render_template('t_dashboard.html',username=session['user']['username'],chall_1=chall_1,chall_2=chall_2)

@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/logout')
def logout():
	session.clear()
	return redirect('/')

@app.route('/submit_flag',methods=['POST'])
@check_login
def submit_flag():
	_id = request.json.get('_id')[-1]
	submitted_flag = request.json.get('challenge_flag')
	chall_details = db.challs.find_one(
			{
			"_id": md5(md5(str(_id).encode('utf-8')).hexdigest().encode('utf-8')).hexdigest(),
			"challenge_flag":submitted_flag
			}
	)
	if chall_details == None:
		return "wrong flag!"
	else:
		return "correct flag!"

# wait untill mongodb start then create the challs in db
sleep(10)
createChalls()