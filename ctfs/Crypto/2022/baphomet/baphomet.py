#!/usr/bin/env python3

from base64 import b64encode
from flag import flag

def encrypt(msg):
	ba = b64encode(msg.encode('utf-8'))
	baph, key = '', ''

	for b in ba.decode('utf-8'):
		if b.islower():
			baph += b.upper()
			key += '0'
		else:
			baph += b.lower()
			key += '1'

	baph = baph.encode('utf-8')
	key = int(key, 2).to_bytes(len(key) // 8, 'big')

	enc = b''
	for i in range(len(baph)):
		enc += (baph[i] ^ key[i % len(key)]).to_bytes(1, 'big')

	return enc

enc = encrypt(flag)
f = open('flag.enc', 'wb')
f.write(enc)
f.close()