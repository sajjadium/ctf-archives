import pickle
import base64
import io
import os

POKEMON = {id: (os.environ.get('FLAG', 'flag{TEST}') if id == 1337 else 'EKANS') for id in range(2000)}
USERS = {'guest': 'guest', 'PokeMaster3000': os.environ.get('ADMIN_PASSWORD', '<secret>')}
ADMINS = ['PokeMaster3000']

class User:
	admin = False

	def __init__(self, username='guest', password='guest'):
		self.username = username
		self.password = password
		if username in ADMINS: self.admin = True

	def is_admin(self): return self.authenticated() and self.admin

	def authenticated(self): return self.password == USERS.get(self.username)

class SafeUnpickler(pickle.Unpickler):
	def find_class(self, module, name):
		if module == "db" and name == "User": return User
		raise pickle.UnpicklingError(f"HACKING DETECTED")

load_user = lambda request: SafeUnpickler(io.BytesIO(base64.b64decode(request.cookies['user'].encode('utf-8')))).load()
