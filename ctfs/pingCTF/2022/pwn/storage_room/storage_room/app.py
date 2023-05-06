from _import import *

app = Flask(__name__)
app.secret_key = secrets.token_hex(0o77)

# Chain and buffer
@app.get('/files')
def files():
	if 'username' in session:
		return render_template('files.html', logged_in=True)
	else:
		return render_template('index.html', message=messages.not_logged, logged_in=False)

@app.post("/files")
def do_files():
	if not 'username' in session:
		return render_template('index.html', message=messages.not_logged, logged_in=False)
	file = request.files.get('file')
	contents = file.read()
	if len(contents) > MAX_NEW_BUFFER_SIZE:
		return render_template('files.html', message=messages.buffer_to_big, logged_in=True)
	else:
		isSuccess = append_buffer(session['username'], contents, 'using_special_buffer' in session and session['using_special_buffer'] == True)
		if isSuccess:
			return render_template('files.html', message=messages.buffer_appended, logged_in=True)
		else:
			return render_template('files.html', message=messages.buffer_append_error, logged_in=True)


@app.get('/chain')
def chain():
	if not 'username' in session:
		return render_template('index.html', message=messages.not_logged, logged_in=False)
	buffer = get_buffer(session['username'])
	if buffer[1]:
		privateUserBuffer = pickle.loads(buffer[0])
		buffer_content = str(privateUserBuffer.get())
		return render_template('chain.html', logged_in=True, buffer=f"{buffer_content}, Length: {len(privateUserBuffer)}, Index: {privateUserBuffer.position()}")
	else:
		buffer_content = ""
		if is_printable(buffer[0]):
			buffer_content = buffer[0].decode()
		else:
			buffer_content = b64encode(buffer[0]).decode()
		return render_template('chain.html', logged_in=True, buffer=buffer_content)

@app.post("/clear")
def do_clear():
	if 'username' in session:
		try:
			clear_buffer(session['username'])
			return messages.buffer_cleared
		except:
			return messages.buffer_clear_error
	else:
		return messages.not_logged

@app.post("/special-buffer")
def do_special_buffer():
	if not 'username' in session:
		return messages.not_logged
	if 'using_special_buffer' in session and session['using_special_buffer']:
		return messages.special_buffer_already_used
	clear_buffer(session['username'])
	userPrivateBuffer = PrivateBufferClass(DEFAULT_BUFFER_SIZE)
	session['using_special_buffer'] = True
	buffer = pickle.dumps(userPrivateBuffer, protocol=5)
	set_buffer(session['username'], buffer)
	return messages.using_special_buffer


# Authentication
@app.get("/authentication")
def authentication():
	return render_template('authentication.html')

@app.post("/authentication")
def do_authenticate():
	username = request.form.get('username', '')
	password = request.form.get('password', '')
	if not is_safe(username) or not is_safe(password):
		return render_template('index.html', message=messages.bad_charactes)
	res = login(username)
	if res:
		if res['password'] == password:
			session['username'] = username
			session['using_special_buffer'] = is_using_special_buffer(username)
			return render_template('index.html', message=messages.logged.replace(':u', username), logged_in=True)
		else:
			return render_template('index.html', message=messages.bad_password)
	else:
		register(username, password)
		session['username'] = username
		return render_template('index.html', message=messages.registered.replace(':u', username), logged_in=True)

# Home
@app.get("/")
def home():
	if 'username' in session:
		return render_template('index.html', logged_in=True)
	else:
		return render_template('index.html', logged_in=False)

@app.get("/logout")
def logout():
	session.pop('username', None)
	return render_template('index.html', message=messages.logged_out, logged_in=False)

@app.before_first_request
def server_start():
	cursor = db().cursor()
	cursor.executescript("DROP TABLE IF EXISTS users")
	db().commit()
	cursor = db().cursor()
	cursor.executescript('''
	CREATE TABLE "users" (
		"id"		INTEGER PRIMARY KEY AUTOINCREMENT,
		"username"  TEXT,
		"password"  TEXT,
		"buffer"	BLOB DEFAULT "Welcome to your buffer!"
	);
	''')
	db().commit()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=3000, debug=False)
