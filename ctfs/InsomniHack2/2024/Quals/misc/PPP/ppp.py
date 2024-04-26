from os import popen
import hashlib, time, math, subprocess, json


def response(res):
	print(res + ' | ' + popen('date').read())
	exit()

def generate_nonce():
	current_time = time.time()
	rounded_time = round(current_time / 60) * 60  # Round to the nearest 1 minutes (60 seconds)
	return hashlib.sha256(str(int(rounded_time)).encode()).hexdigest()

def is_valid_proof(data, nonce):
	DIFFICULTY_LEVEL = 6
	guess_hash = hashlib.sha256(f'{data}{nonce}'.encode()).hexdigest()
	return guess_hash[:DIFFICULTY_LEVEL] == '0' * DIFFICULTY_LEVEL


class Blacklist:

	def __init__(self, data, nonce):
		self.data = data
		self.nonce = nonce

	def get_data(self):
		out = {}
		out['data'] = self.data if 'data' in self.__dict__ else ()
		out['nonce'] = self.nonce if 'nonce' in self.__dict__ else ()
		return out


def add_to_blacklist(src, dst):
	for key, value in src.items():
		if hasattr(dst, '__getitem__'):
			if dst[key] and type(value) == dict:
				add_to_blacklist(value, dst.get(key))
			else:
				dst[key] = value
		elif hasattr(dst, key) and type(value) == dict:
			add_to_blacklist(value, getattr(dst, key))
		else:
			setattr(dst, key, value)

def lists_to_set(data):
	if type(data) == dict:
		res = {}
		for key, value in data.items():
			res[key] = lists_to_set(value)
	elif type(data) == list:
		res = ()
		for value in data:
			res = (*res, lists_to_set(value))
	else:
		res = data
	return res

def is_blacklisted(json_input):

	bl_data = blacklist.get_data()
	if json_input['data'] in bl_data['data']:
		return True
	if json_input['nonce'] in bl_data['nonce']:
		return True

	json_input = lists_to_set(json_input)
	add_to_blacklist(json_input, blacklist)
	return False


if __name__ == '__main__':

	blacklist = Blacklist(['dd9ae2332089200c4d138f3ff5abfaac26b7d3a451edf49dc015b7a0a737c794'], ['2bfd99b0167eb0f400a1c6e54e0b81f374d6162b10148598810d5ff8ef21722d'])

	try:
		json_input = json.loads(input('Prove your work 😼\n'))
	except Exception:
		response('no')

	if not isinstance(json_input, dict):
		response('message')

	data = json_input.get('data')
	nonce = json_input.get('nonce')
	client_hash = json_input.get('hash')

	if not (data and nonce and client_hash):
		response('Missing data, nonce, or hash')

	server_nonce = generate_nonce()
	if server_nonce != nonce:
		response('nonce error')

	if not is_valid_proof(data, nonce):
		response('Proof of work is invalid')

	server_hash = hashlib.sha256(f'{data}{nonce}'.encode()).hexdigest()
	if server_hash != client_hash:
		response('Hash does not match')

	if is_blacklisted(json_input):
		response('blacklisted PoW')

	response('Congratulation, You\'ve proved your work 🎷🐴')
