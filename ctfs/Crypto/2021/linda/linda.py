#!/usr/bin/env python3

from Crypto.Util.number import *
from math import gcd
from flag import flag

def keygen(p):
	while True:
		u = getRandomRange(1, p)
		if pow(u, (p-1) // 2, p) != 1:
			break
	x = getRandomRange(1, p)
	w = pow(u, x, p)
	while True:
		r = getRandomRange(1, p-1)
		if gcd(r, p-1) == 1:
			y = x * inverse(r, p-1) % (p-1)
			v = pow(u, r, p)
			return u, v, w
	
def encrypt(m, pubkey):
	p, u, v, w = pubkey
	assert m < p
	r, s = [getRandomRange(1, p) for _ in '01']
	ca = pow(u, r, p)
	cb = pow(v, s, p)
	cc = m * pow(w, r + s, p) % p
	enc = (ca, cb, cc)
	return enc

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "+"
	pr(border*72)
	pr(border, "  .:::::: LINDA Cryptosystem has high grade security level ::::::.  ", border)
	pr(border, "  Can you break this cryptosystem and find the flag?                ", border)
	pr(border*72)

	pr('| please wait, preparing the LINDA is time consuming...')
	from secret import p
	u, v, w = keygen(p)
	msg = bytes_to_long(flag)
	pubkey = p, u, v, w
	enc = encrypt(msg, pubkey)
	while True:
		pr("| Options: \n|\t[E]xpose the parameters \n|\t[T]est the encryption \n|\t[S]how the encrypted flag \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'e':
			pr(f'| p = {p}')
			pr(f'| u = {u}')
			pr(f'| v = {v}')
			pr(f'| w = {w}')
		elif ans == 's':
			print(f'enc = {enc}')
		elif ans == 't':
			pr('| send your message to encrypt: ')
			m = sc()
			m = bytes_to_long(m.encode('utf-8'))
			pr(f'| encrypt(m) = {encrypt(m, pubkey)}')
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()