#!/usr/bin/env python3

from Crypto.PublicKey import RSA
from Crypto.Util import number
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys
from secret import flag

MAX_COUNT = 128

key = RSA.generate(2048, e = 1337)

def loop():
	print('My public modulus is:\n%d' % key.n)
	print('Let me count how long it takes you to find the flag.')

	for counter in range(MAX_COUNT):
		message = 'So far we had %03d failed attempts to find the secret flag %s' % (counter, flag)
		print(pow(bytes_to_long(message.encode()), key.e, key.n))
		print('What is your guess?')
		sys.stdout.flush()
		guess = sys.stdin.buffer.readline().strip()
		if guess.decode() == flag:
			print('Congratulations for finding the flag after %03d rounds.' % counter)
			sys.stdout.flush()
			return

if __name__ == '__main__':
	try:
		loop()
	except Exception as err:
		print(repr(err))
