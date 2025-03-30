#!/usr/local/bin/python

import hashlib
import secrets
from Crypto.PublicKey import RSA
from Crypto.Util.strxor import strxor

DEATH_CAUSES = [
	'a fever',
	'dysentery',
	'measles',
	'cholera',
	'typhoid',
	'exhaustion',
	'a snakebite',
	'a broken leg',
	'a broken arm',
	'drowning',
]

def encrypt(k, msg):
	key = k.to_bytes(1024//8, 'big')
	msg = msg.encode().ljust(64, b'\x00')
	pad = hashlib.shake_256(key).digest(len(msg))
	return strxor(pad, msg)

def run_ot(key, msg0, msg1):
	'''
	https://en.wikipedia.org/wiki/Oblivious_transfer#1–2_oblivious_transfer
	'''
	x0 = secrets.randbelow(key.n)
	x1 = secrets.randbelow(key.n)
	print(f'n: {key.n}')
	print(f'e: {key.e}')
	print(f'x0: {x0}')
	print(f'x1: {x1}')
	v = int(input('v: '))
	assert 0 <= v < key.n, 'invalid value'
	k0 = pow(v - x0, key.d, key.n)
	k1 = pow(v - x1, key.d, key.n)
	c0 = encrypt(k0, msg0)
	c1 = encrypt(k1, msg1)
	print(f'c0: {c0.hex()}')
	print(f'c1: {c1.hex()}')

if __name__ == '__main__':
	with open('flag.txt') as f:
		flag = f.read().strip()

	with open('key.pem', 'rb') as f:
		key = RSA.import_key(f.read())

	print('=== CHOOSE YOUR OWN ADVENTURE: Winxy Pistol Edition ===')
	print('you enter a cave.')

	for _ in range(64):
		print('the tunnel forks ahead. do you take the left or right path?')
		msgs = [None, None]
		page = secrets.randbits(32)
		live = f'you continue walking. turn to page {page}.'
		die = f'you die of {secrets.choice(DEATH_CAUSES)}.'
		msgs = (live, die) if secrets.randbits(1) else (die, live)
		run_ot(key, *msgs)
		page_guess = int(input('turn to page: '))
		if page_guess != page:
			exit()

	print(f'you find a chest containing {flag}')
