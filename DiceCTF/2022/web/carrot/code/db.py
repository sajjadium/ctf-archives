import plyvel
import json
import bcrypt
import secrets
import os
import config

db = plyvel.DB('database', create_if_missing=True)

def has(user):
	if db.get(user.encode()) is None:
		return False
	return True

def get(user):
	return json.loads(db.get(user.encode()).decode())

def put(user, value):
	return db.put(user.encode(), json.dumps(value).encode())

if not has('admin'):
	password = config.ADMIN_PASSWORD
	
	put('admin', {
		'tasks': [{
			'title': 'flag',
			'content': os.getenv('FLAG', default='dice{flag}'),
			'priority': 1,
			'id': 0
		}],
		'password': bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')
	})