from nis import cat
from flask import Flask, render_template, request, redirect, session, flash, url_for, g, abort
import sqlite3
from uuid import uuid4
import os
import re

DATABASE = './database.db'

app = Flask(__name__)
app.secret_key = os.urandom(24)

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('./schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('error.html', error=404)

@app.errorhandler(500)
def pageNotFound(error):
    return render_template('error.html', error=500)

@app.route('/', methods=['GET', 'POST'])
def home():
	#display approved threads
	cur = get_db().execute("SELECT title, thread FROM threads where verified = 1")
	threads = cur.fetchall()
	cur.close()
	return render_template('index.html', threads=threads)

@app.route('/thread', methods=['POST'])
def thread():
	if 'title' in request.form and 'thread' in request.form:
		title = request.form['title']
		thread = request.form['thread']
		thread = re.sub(r"<script[\s\S]*?>[\s\S]*?<\/script>", "", thread, flags=re.IGNORECASE)
		thread = re.sub(r"<img[\s\S]*?>[\s\S]*?<\/img>", "", thread, flags=re.IGNORECASE)
		thread_uuid = str(uuid4())
		cur = get_db().cursor()
		cur.execute("INSERT INTO threads ( id, title, thread) VALUES ( ?, ?, ?)", (thread_uuid, title, thread))
		get_db().commit()
		cur.close()
		return redirect(url_for('view', id=thread_uuid))
	return redirect(url_for('home')) , 400


@app.route('/view', methods=['GET'])
def view():
	if 'id' in request.args:
		thread_uuid = request.args.get('id')
		cur = get_db().execute("SELECT title, thread FROM threads WHERE id = ?", (thread_uuid,))
		result = cur.fetchone()
		cur.close()
		if result:
			return render_template('thread.html', thread_uuid=thread_uuid, result=result)
		return abort(404)
	return redirect(url_for('home')) , 400


''' ADMIN PANEL '''
@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('admin'))

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		cur = get_db().execute("SELECT * FROM users WHERE username = ?", (username,))
		user = cur.fetchone()
		cur.close()
		if user and (password.encode('utf-8')== user[2].encode('utf-8')):
			session['username'] = user[1]
			session['user_id'] = user[0]
			return redirect(url_for('admin'))
		else:
			flash('Invalid login credentials')
			return redirect(url_for('login'))

	return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
	if 'username' not in session:
		return redirect(url_for('login'))
	#view analytics
	if 'query' in request.args:
		query = request.args.get('query')
		try:
			cur = get_db().execute("SELECT count(*) FROM {0}".format(query))
		except:
			return render_template('adminPanel.html') , 500
		result = cur.fetchall()
		cur.close()
		return render_template('adminPanel.html', result=result, param=query)	
	else:
		return render_template('adminPanel.html')

# TODO add 'verify thread' endpoint

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('user_id', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	init_db()
	app.run("0.0.0.0", debug=False, port=80)