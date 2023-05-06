from hashlib import sha1
from random import *
from sys import exit
from os import urandom
from Crypto.PublicKey import DSA
from Crypto.Util.number import *

rot = randint(2, 2**160 - 1)
chop = getPrime(159)


def message_hash(x):
	return bytes_to_long(sha1(x).digest())


def nonce(s, padding, i, q):
	return (pow(message_hash(s), rot, chop) + padding + i)%q


def verify(r, s, m):
	if not (0 < r and r < q and 0 < s and s < q):
		return False
	w = pow(s, q - 2, q)
	u1 = (message_hash(m) * w) % q
	u2 = (r * w) % q
	v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
	return v == r

def pow_solve():
	pow_nonce = urandom(4)
	print(f"Solve PoW for {pow_nonce.hex()}")
	inp = bytes.fromhex(input())
	if sha1(pow_nonce + inp).hexdigest().endswith('000000'):
		print("Correct PoW. Continue")
		return True
	print("Incorrect PoW. Abort")
	return False


try:
	if not pow_solve():
		exit()
	L, N = 1024, 160
	dsakey = DSA.generate(1024)
	p = dsakey.p
	q = dsakey.q
	h = randint(2, p - 2)

	# sanity check
	g = pow(h, (p - 1) // q, p)
	if g == 1:
		print("oopsie")
		exit(1)

	x = randint(1, q - 1)
	y = pow(g, x, p)

	print(f"<p={p}, q={q}, g={g}, y={y}>")

	pad = randint(1, 2**160)
	signed = []
	for i in range(2):
		print("what would you like me to sign? in hex, please")
		m = bytes.fromhex(input())
		if m == b'give flag' or m == b'give me all your money':
			print("haha nice try...")
			exit()
		if m in signed:
			print("i already signed that!")
			exit()
		signed.append(m)
		# nonce generation remains the same
		k = nonce(m, pad, i, q)
		if k < 1:
			exit()
		r = pow(g, k, p) % q
		if r == 0:
			exit()
		s = (pow(k, q - 2, q) * (message_hash(m) + x * r)) % q
		if s == 0:
			exit()
		# No hash leak for you this time
		print(f"<r={r}, s={s}>")

	print("ok im done for now. You visit the flag keeper...")
	print("for flag, you must bring me signed message for 'give flag'")

	r1 = int(input())
	s1 = int(input())
	if verify(r1, s1, b"give flag"):
		print(open("flag.txt").read())
	else:
		print("Never gonna give you up")
except:
	print("Never gonna let you down")
