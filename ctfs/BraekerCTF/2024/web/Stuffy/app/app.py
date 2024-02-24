## Stuffy, a social media platform for sharing thoughts
### 


import sqlite3
import urllib3
import string
import uuid

from flask import Flask, render_template, request, make_response
from random import choice


# init app
app = Flask(__name__)

# read flag
flag = open('flag.txt','r').read()

# load username prefixes
usernames = open('usernames.txt','r').readlines()

# init db
conn = sqlite3.connect('file::memory:?cache=shared', check_same_thread=False)

# create API key
internal_api_key = str(uuid.uuid4())


# check if username exists in database
def does_profile_exist(username):

	sql = '''SELECT id from profiles where username = ?'''
	cur = conn.cursor()
	cur.execute(sql, [username])

	ret = cur.fetchone()
	if ret != None:
		return True
	else:
		return False


# create new profile
def create_profile():

	user_ip = request.remote_addr
	new_username = choice(usernames).strip() + \
		''.join(choice(string.ascii_letters) for i in range(4))

	cur = conn.cursor()

	sql = '''DELETE FROM profiles WHERE ip = ?'''
	cur.execute(sql, (user_ip, ))

	sql = '''INSERT INTO profiles (username, stuff, ip) VALUES (?,?,?)'''
	cur.execute(sql, (new_username, '', user_ip))

	conn.commit()

	return new_username


# get stuff for username
def get_stuff(username):

	sql = '''SELECT stuff from profiles where username = "''' + username + '''"'''
	cur = conn.cursor()
	cur.execute(sql)

	ret = cur.fetchone()
	if ret != None:
		return ret[0]
	else:
		return ''


# select stuffs from users
def get_latest_stuff():

	sql = "SELECT username,stuff from profiles WHERE stuff not LIKE ? ORDER BY username DESC LIMIT 40"
	cur = conn.cursor()
	cur.execute(sql, ["%%%s%%" % flag])

	stuff = cur.fetchmany(size=40)

	return stuff


# prevent vulnerabilities
def security_filter(value):

	# prevent xss
	value = value.replace('<','')
	value = value.replace('>','')

	# prevent sqli
	value = value.replace('\'','')

	# prevent too much stuff
	if len(value) > 256:
		value = value[:256]
	
	return value


# give flag to a user (for internal use)
@app.route("/give_flag", methods=["POST"])
def give_flag():

	username = request.form.get('username')

	if request.headers['X-Real-IP'] == "127.0.0.1":

		sql = '''UPDATE profiles SET stuff = ? WHERE username = ?'''
		cur = conn.cursor()
		cur.execute(sql, (flag, username))
		conn.commit()

		return 'congrats!'

	else:
		sql = '''UPDATE profiles SET stuff = ? WHERE username = ?'''
		cur = conn.cursor()
		cur.execute(sql, ('No stuff for you', username))
		conn.commit()

		return 'no congrats!'


# update stuff for a user (for internal use)
@app.route("/update_profile_internal", methods=["POST"])
def update_profile_internal():

	api_key = request.form.get('api_key')
	username = request.form.get('username')
	stuff = request.form.get('stuff')

	add_emoji = request.headers.get('emoji')
	if add_emoji:
		if add_emoji == 'cow':
			stuff += ' 🐄'
		if add_emoji == 'cat':
			stuff += ' 🐱'
		if add_emoji == 'fish':
			stuff += ' 🐠'
	add_image = request.headers.get('image')
	if add_image:
		if add_image == 'cow':
			stuff += '<img id="mood" src="/static/images/cow.png">'
		if add_image == 'cat':
			stuff += '<img id="mood" src="/static/images/cat.png">'
		if add_image == 'fish':
			stuff += '<img id="mood" src="/static/images/fish.png">'

	if api_key == internal_api_key:

		sql = '''UPDATE profiles SET stuff = ? WHERE username = ?'''
		cur = conn.cursor()
		cur.execute(sql, (stuff, username))
		conn.commit()

		return 'Updated profile'

	else:
		return render_template('forbidden.html', reason='wrong key')


# show the latest stuff
@app.route("/view_stuff", methods=["GET"])
def view_stuffs():
	username = request.cookies.get('username')

	if username and does_profile_exist(username):
		stuff = get_latest_stuff()
		return render_template('view_stuff.html', stuff=stuff)

	else:
		return render_template('forbidden.html', reason='you don\'t have an active user profile')


# show user stuff or create a new user
@app.route("/")
def index() -> str:
	username = request.cookies.get('username')

	if username and does_profile_exist(username):
		stuff = get_stuff(username)

		return make_response(render_template('wb.html', username=username, stuff=stuff))
	
	else:
		username = create_profile()

		msg = "New user created: %s" % username
		resp = make_response(render_template('wb.html', msg=msg, username=username, stuff=''))
		resp.set_cookie('username', username)

		return resp


# set a user's stuff
@app.route('/set_stuff', methods=["POST"])
def set_stuff():

	username = request.cookies.get('username')
	
	if not username:
		return render_template('forbidden.html', reason='no username provided')

	if not does_profile_exist(username):
		return render_template('forbidden.html', reason='username does not exist')

	stuff = request.form.get('stuff')

	if len(stuff) > 200:
		return render_template('forbidden.html', reason='too much stuff')

	special_type = request.form.get('special_type')
	special_val = request.form.get('special_val')

	if username and stuff and special_type and special_val:

		# do security
		stuff = security_filter(stuff)
		special_type = security_filter(special_type)
		special_val = security_filter(special_val)
		username = security_filter(username)

		# Update stuff internally
		post_body = 'api_key=%s&username=%s&stuff=%s' % (internal_api_key,username,stuff)

		http = urllib3.PoolManager()
		url = 'http://127.0.0.1:3000/update_profile_internal'
		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			special_type: special_val
		}
		response = http.request("POST", url, body=post_body, headers=headers)

		return render_template('stuff_saved.html')
	else:
		return render_template('forbidden.html', reason='no stuff provided')


def main():
	cur = conn.cursor()
	cur.execute("""
		create table profiles(
			id integer primary key autoincrement not null,
			username text,
			stuff text,
			ip text
		);
	""")
	conn.commit()
	app.run('0.0.0.0', 2000, threaded=True)

if __name__ == "__main__":
	main()
