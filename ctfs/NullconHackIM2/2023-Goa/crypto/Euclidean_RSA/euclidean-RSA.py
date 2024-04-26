#!/usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long
from secret import flag, magic

while True:
	try:
		key = RSA.generate(2048)
		a,b,c,d = magic(key)
		break
	except:
		pass
assert a**2 + b**2 == key.n
assert c**2 + d**2 == key.n
for _ in [a,b,c,d]:
	print(_)
cipher = pow(bytes_to_long(flag), key.e, key.n)
print(cipher)
