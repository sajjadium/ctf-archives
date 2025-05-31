#!/usr/bin/env python3

import sys, time
from Crypto.Util.number import *
from secret import decrypt, FLAG

def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc(): 
	return sys.stdin.buffer.readline()

def jam(x, y, d, n):
	x1, y1 = x
	x2, y2 = y
	_jam = (x1 * x2 + d * y1 * y2, x1 * y2 + x2 * y1)
	return (_jam[0] % n, _jam[1] % n)

def keygen(nbit):
	p, q = [getPrime(nbit) for _ in '01']
	a = getRandomRange(1, p * q)
	pkey = p * q
	skey = (p, q)
	return pkey, skey

def polish(skey, l):
	nbit = skey[0].bit_length()
	PLS = [skey[getRandomRange(0, 2)] * getPrime(nbit) + getRandomNBitInteger(nbit >> 1) for _ in range(l)]
	return PLS

def encrypt(m, pubkey):
	n = pubkey
	e, r = 65537, getRandomRange(1, n)
	s = r * m % n
	u = (s + inverse(s, n)) * inverse(2, n) % n
	a = (inverse(s, n) - u) * inverse(m, n) % n
	d = pow(a, 2, n)
	c, f = (1, 0), 1
	for _ in range(e):
		c = jam(c, (u, m), d, n)
		f = f * a % n
	return c, f

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, ".::               Welcome to N0PSichu challenge!              ::. ", border)
	pr(border, " You should analyze this cryptosystem and braek it to get the flag", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	nbit = 512
	pkey, skey = keygen(nbit)
	m = bytes_to_long(FLAG)
	enc = encrypt(m, pkey)
	_m = decrypt(enc, skey)

	while long_to_bytes(_m) == FLAG:
		pr("| Options: \n|\t[E]ncrypt \n|\t[I]formations \n|\t[P]olish the keys \n|\t[Q]uit")
		ans = sc().decode().strip().lower()
		if ans == 'e':
			pr(border, 'please send your message to encrypt: ')
			_m = sc().decode().strip()
			try:
				_m = int(_m)
			except:
				die(border, 'Your input is not correct! Bye!')
			_m = _m % pkey
			_enc = encrypt(_m, pkey)
			pr(border, f'enc = {_enc}')
		elif ans == 'i':
			pr(border, f'pkey = {pkey}')
			pr(border, f'encrypted_flag = {enc}')
		elif ans == 'p':
			pr(border, 'Please let me know how many times you want to polish and burnish the key: ')
			l = sc().decode().strip()
			chance = int(str(time.time())[-2:])
			try:
				l = int(l) % chance
			except:
				die(border, 'Please be polite! Bye!!')
			PLS = polish(skey, l)
			i = 0
			for pls in PLS:
				pr(border, f'PLS[{i}] = {PLS[i]}')
				i += 1
		elif ans == 'q': die(border, "Quitting...")
		else: die(border, "Bye...")

if __name__ == '__main__':
	main()