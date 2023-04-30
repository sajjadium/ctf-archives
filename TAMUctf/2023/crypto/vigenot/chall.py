import re
from flag import flag, key

alpha = 'abcdefghijklmnopqrstuvwxyz'
regex = re.compile('[^a-zA-Z]')

msg = flag
key = key

def encrypt(msg, key):
	ctxt = ''

	msg = regex.sub('', msg).lower()
	key = regex.sub('', key).lower()

	for i in range(len(msg)):
		index = alpha.index(msg[i]) ^ alpha.index(key[i % len(key)])
		if index < 26:
			ctxt += alpha[index]
		else:
			ctxt += msg[i]
		
		if i % len(key) == len(key) - 1:
			key = key[1:] + key[0]

	return ctxt

c = encrypt(msg, key)

print("encrypted message: %s" % c)
