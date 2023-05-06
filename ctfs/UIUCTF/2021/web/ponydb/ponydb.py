from flask import Flask, render_template, session, request, redirect, flash
import mysql.connector
import secrets
import time
import json
import os

app = Flask(__name__)
app.secret_key = os.environ['SECRET_KEY']

flag = os.environ['FLAG']

config = {
	'host': os.environ['DB_HOST'],
	'user': os.environ['DB_USER'],
	'password': os.environ['DB_PASS'],
	'database': os.environ['DB'],
	'sql_mode': 'NO_BACKSLASH_ESCAPES'
}

for i in range(30):
	try:
		conn = mysql.connector.connect(**config)
		break
	except mysql.connector.errors.DatabaseError:
		time.sleep(1)
else: conn = mysql.connector.connect(**config)
cursor = conn.cursor()
try: cursor.execute('CREATE TABLE `ponies` (`name` varchar(64), `bio` varchar(256), '
                    '`image` varchar(256), `favorites` varchar(256), `session` varchar(64))')
except mysql.connector.errors.ProgrammingError: pass
cursor.close()
conn.close()

@app.route('/')
def ponies():
	cnx = mysql.connector.connect(**config)
	cur = cnx.cursor()

	if 'id' not in session:
		session['id'] = secrets.token_hex(32)
		cur.execute("INSERT INTO `ponies` VALUES ('Pwny', 'Pwny is the official mascot of SIGPwny!', "
		            "'https://sigpwny.github.io/images/logo.png', " + \
		            f"'{{\"color\":\"orange\",\"word\":\"pwn\",\"number\":13}}', '{session['id']}')")
		cnx.commit()

	ponies = []
	cur.execute(f"SELECT * FROM `ponies` WHERE session='{session['id']}'")
	for (name, bio, image, data, _) in cur:
		ponies.append({"name": name, "bio": bio, "image": image, "favorites": json.loads(data)})

	cur.close()
	cnx.close()
	return render_template('ponies.html', ponies=ponies, flag=flag)

@app.route('/pony', methods=['POST'])
def add():
	error = None

	name = request.form['name']
	if "'" in name: error = 'Name may not contain single quote'
	if len(name) > 64: error = 'Name too long'

	bio = request.form['bio']
	if "'" in bio: error = 'Bio may not contain single quote'
	if len(bio) > 256: error = 'Bio too long'

	image = request.form['image']
	if "'" in image: error = 'Image URL may not contain single quote'
	if len(image) > 256: error = 'Image URL too long'

	favorite_key = request.form['favorite_key']
	if "'" in favorite_key: error = 'Custom favorite name may not contain single quote'
	if len(favorite_key) > 64: 'Custom favorite name too long'

	favorite_value = request.form['favorite_value']
	if "'" in favorite_value: error = 'Custom favorite may not contain single quote'
	if len(favorite_value) > 64: 'Custom favorite too long'

	word = request.form['word']
	if "'" in word: error = 'Word may not contain single quote'
	if len(word) > len('antidisestablishmentarianism'): error = 'Word too long'

	number = int(request.form['number'])
	if number >= 100: error = "Ponies can't count that high"
	if number < 0: error = "Ponies can't count that low"

	if error: flash(error)
	else:
		cnx = mysql.connector.connect(**config)
		cur = cnx.cursor()
		cur.execute(f"INSERT INTO `ponies` VALUES ('{name}', '{bio}', '{image}', " + \
		            f"'{{\"{favorite_key.lower()}\":\"{favorite_value}\"," + \
		            f"\"word\":\"{word.lower()}\",\"number\":{number}}}', " + \
		            f"'{session['id']}')")
		cnx.commit()
		cur.close()
		cnx.close()

	return redirect('/')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=1337, threaded=True)
