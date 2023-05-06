import string, re

WHITE_LIST = string.ascii_letters + string.digits
BLACK_LIST = [
 'class', 'mro', 'base', 'request', 'app',
 'sleep', 'add', '+', 'config', 'subclasses', 'format', 'dict', 'get', 'attr', 'globals', 'time', 'read',
 'import', 'sys', 'cookies', 'headers', 'doc', 'url', 'encode', 'decode', 'chr', 'ord', 'replace', 'echo',
 'pop', 'builtins', 'self', 'template', 'print', 'exec', 'response', 'join', '{}', '%s', '\\', '*', '#', '&']

def valid_register(username, password):
	for char in (
	 username, password):
		if char not in WHITE_LIST:
			return False
	else:
		if re.search('^[0-9a-zA-Z]+$', username) or (re.search('^[0-9a-zA-Z]+$', password)):
			return False
		return True


def countChar(picture):
	if picture.count('.') > 1:
		return False
	if picture.count(',') > 1:
		return False
	if picture.count(':') > 1:
		return False
	for i in range(0,len(picture)):
		if picture[i] == "'" or picture[i] == '"':
			if picture[i+1] == "'" or picture[i+1] == '"':
				return False
	return True

def check_len(picture):
	if len(picture) > 56:
		return False
	return True


def isValid(picture):
	picture = picture.lower()
	if countChar(picture) and len(picture) <= 202:
		for char in picture:
			if char in string.digits:
				return False
		for i in BLACK_LIST:
			if i in picture:
				return False
		return True
	return False