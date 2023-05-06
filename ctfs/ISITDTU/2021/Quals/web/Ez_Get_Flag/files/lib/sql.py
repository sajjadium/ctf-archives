import sqlite3
import hashlib

def login_check(username, password):
	conn = sqlite3.connect('database/users.db')
	row = conn.execute("SELECT * from users where username = ? and password = ?", (username, hashlib.sha1(password.encode()).hexdigest(), )).fetchall()
	return len(row)

def reg(username,password):
	conn = sqlite3.connect('database/users.db')
	row = conn.execute("SELECT username from users where username = ?",(username)).fetchall()
	if len(row) < 1:
		return "Account exits !!!"
	else:
		result = conn.execute("INSERT INTO users VALUE (?,?)",(username,hashlib.sha1(password.encode()).hexdigest()))
		if result:
			return 'Sign Up Success !!!'
		else:
			return 'Sign Up Failed !!!'