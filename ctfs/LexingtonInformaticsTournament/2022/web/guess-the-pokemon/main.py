import sqlite3
from flask import Flask, render_template, render_template_string, redirect, url_for, request

con = sqlite3.connect('data.db', check_same_thread=False)
app = Flask(__name__)

cur = con.cursor()
# comment
cur.execute('''DROP TABLE IF EXISTS pokemon''')
cur.execute('''CREATE TABLE pokemon (names text)''')
cur.execute(
    '''INSERT INTO pokemon (names) VALUES ("[FLAG REDACTED]") '''
)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        name = request.form['name']

        if ("'" in name or "\\" in name or '"' in name):
          return render_template('login.html', error="no quotes or backslashes:)")
        elif (name == "names"):
          return render_template('login.html', error="you are wrong :<")
			
        try:
          cur.execute("SELECT * FROM pokemon WHERE names=" + name + "")
        except:
          render_template('login.html', error="you are wrong :3")
				
		
				
        rows = cur.fetchall()

        
        if len(rows) > 0:
            return render_template('login.html',
                                   error="Correct! The poekmon was " +
                                   rows[0][0])
        else:
            return render_template('login.html', error="you are wrong :<")

    return render_template('login.html', error="")
