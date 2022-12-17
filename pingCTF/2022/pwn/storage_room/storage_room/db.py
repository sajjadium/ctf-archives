import string
from _import import g, sqlite3, pickle, pickletools
import messages
from app import app
MAX_BUFFER_SIZE = 0xffff

def db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect('/tmp/db2.sqlite3')
		db.row_factory = sqlite3.Row
	return db

def process_buffer(current_buffer, buffer, isSpecialBuffer):
	if not isSpecialBuffer:
		new_buffer = current_buffer + buffer
		if len(new_buffer) > MAX_BUFFER_SIZE:
			return new_buffer[MAX_BUFFER_SIZE:]
		else:
			return new_buffer
	else:
		specialBuffer = pickle.loads(current_buffer)
		specialBuffer.add(buffer)
		return pickle.dumps(specialBuffer, protocol=5)

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

def append_buffer(username, buffer, isSpecialBuffer):
	try:
		cursor = db().cursor()
		query = f"SELECT buffer FROM users WHERE username = '{username}'"
		res = cursor.execute(query).fetchone()
		if res:
			current_buffer = res['buffer']
			try:
				# Ensure bytes
				current_buffer = current_buffer.encode()
				buffer = buffer.encode()
			except:
				pass
			buffer = process_buffer(current_buffer, buffer, isSpecialBuffer)
			set_buffer(username, buffer)
			return True
		else:
			return False
	except Exception as e:
		print(e)
		return False

def set_buffer(username, buffer):
	cursor = db().cursor()
	query = f"UPDATE users SET buffer = ? WHERE username = '{username}'"
	cursor.execute(query, (buffer,))
	db().commit()

def get_buffer(username):
	try:
		cursor = db().cursor()
		query = f"SELECT buffer FROM users WHERE username = '{username}'"
		res = cursor.execute(query).fetchone()
		if res:
			buffer = res['buffer']
			try:
				buffer = buffer.encode()
			except:
				pass
			return (buffer, is_safe_buffer(buffer))
		else:
			return (messages.are_you_logged, False)
	except:
		return messages.invalid_buffer

def is_using_special_buffer(username):
	buffer = get_buffer(username)
	return buffer[1]

def is_safe_buffer(buffer):
	return buffer[:2] == b'\x80\x05' and not pickle.REDUCE in get_buffer_opcodes(buffer)

def clear_buffer(username):
	buffer = get_buffer(username)
	if buffer[1]:
		userBuffer = pickle.loads(buffer[0])
		userBuffer.clear()
		buffer = pickle.dumps(userBuffer, protocol=5)
		set_buffer(username, buffer)
	else:
		set_buffer(username, b'Welcome to your buffer! (Again...)')

def is_printable(s):
	try:
		return all(chr(c) in string.printable for c in s)
	except:
		return False

def get_buffer_opcodes(buffer):
	try:
		opcodes = []
		for _opcode_information, _value, opcode in pickletools.genops(buffer):
			opcodes.append(opcode)
		return opcodes
	except:
		return []

def register(username, password):
	cursor = db().cursor()
	query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
	cursor.execute(query)
	db().commit()

def login(username):
	cursor = db().cursor()
	query = f"SELECT password FROM users WHERE username = '{username}'"
	return cursor.execute(query).fetchone()
