#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys
from secret import flag

key = RSA.generate(2048, e = 3)

def encrypt(msg : bytes, key) -> int:
	m = bytes_to_long(msg)
	if m.bit_length() + 128 > key.n.bit_length():
		return 'Need at least 128 Bit randomness in padding'
	shift = key.n.bit_length() - m.bit_length() - 1
	return pow(m << shift | number.getRandomInteger(shift), key.e, key.n)

def loop():
	print('My public modulus is:\n%d' % key.n)
	print('Here is your secret message:')
	print(encrypt(flag, key))

	while True:
		print('You can also append a word on your own:')
		sys.stdout.flush()
		PS = sys.stdin.buffer.readline().strip()
		print('With these personal words the cipher is:')
		print(encrypt(flag + PS, key))

if __name__ == '__main__':
	try:
		loop()
	except Exception as err:
		print(repr(err))
