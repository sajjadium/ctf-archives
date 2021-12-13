from flask import Flask, render_template, session, request, redirect, flash, make_response, jsonify
import mysql.connector
import secrets
import time
import json
import os
import subprocess
import sys
from datetime import datetime
app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

flag = os.environ['FLAG']
realAdminKey = os.environ['KEY']
config = {
	'host': os.environ['DB_HOST'],
	'user': os.environ['DB_USER'],
	'password': os.environ['DB_PASS'],
	'database': os.environ['DB'],
	'sql_mode': 'NO_BACKSLASH_ESCAPES'
}
adminKeys=[realAdminKey]
for i in range(30):
	try:
		conn = mysql.connector.connect(**config)
		break
	except mysql.connector.errors.DatabaseError:
		time.sleep(1)
else: conn = mysql.connector.connect(**config)
cursor = conn.cursor()
try: cursor.execute('CREATE TABLE `tracking` (`id` varchar(600),`time` varchar(64),`place` varchar(64))')
except mysql.connector.errors.ProgrammingError: pass
try: cursor.execute('CREATE TABLE `flag` (`flag` varchar(600))')
except mysql.connector.errors.ProgrammingError: pass


cursor.close()
conn.close()

@app.route('/')
def outofbounds():
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    
    id=request.cookies.get('id')
    if id:
        if("'" in id):
            return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        now = datetime.now()

        current_time = now.strftime("%H:%M:%S")
        cur.execute(f"INSERT INTO tracking VALUES ('{id}','{current_time}','/')")
         
        
       

    else:
        id= secrets.token_hex(32)
        cur.execute(f"INSERT INTO flag VALUES ('{flag}')")
    cnx.commit()
    cur.close()
    cnx.close()
    toSay= request.args.get('toSay')
    resp = make_response(render_template('escalator.html',toSay=toSay))
    resp.set_cookie('id',id)

    return resp
def convertTuple(tup):
        # initialize an empty string
    str = ''
    for item in tup:
        str = str + item
    return str
@app.route('/trackinfo')
def getInfo():
    cnx = mysql.connector.connect(**config)
    cur = cnx.cursor()
    query = request.args.get('query')
    id=request.cookies.get('id')
    if("'" in id):
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    if(id not in adminKeys):
        return render_template('accessdenied.html')
               
    
    cur.execute(query)
    rows = []
    for resp in cur:
        rows.append(convertTuple(resp))

    cur.close()
    cnx.close()
    return jsonify(rows)

@app.route('/admin', methods=['POST','GET'])
def signOut():
    if (not request.args.get('inputtext')):
        return render_template('clear.html')
    
    resp = make_response(redirect('/'))
    if(request.args.get('inputtext') in adminKeys):
        adminKeys.pop(adminKeys.index(request.args.get('inputtext')))
    
    return resp

@app.route('/report', methods=['GET', 'POST'])
def report():
    
    if request.method == 'GET':
        return render_template('report.html')

    url = request.form.get('url')
    if not url:
        
        return render_template('report.html',str='url is required')
    if not url.startswith('http://'):
        
        return render_template('report.html',str='invalid url')
    id= secrets.token_hex(32)
    
    adminKeys.append(id)
    subprocess.Popen(['node', 'bot.js', url,id], shell=False)
    flash('Admin is visiting your link!')
    return render_template('report.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1337, threaded=True)
