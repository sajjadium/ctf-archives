#!/usr/bin/env python3

from Crypto.Util.number import *
from hashlib import sha256
import ecdsa
from flag import FLAG

E = ecdsa.SECP256k1
G, n = E.generator, E.order

cryptonym = b'Persian Gulf'

def keygen(n, G):
	privkey = getRandomRange(1, n-1)
	pubkey = privkey * G
	return (pubkey, privkey)

def sign(msg, keypair):
	nbit, dbit = 256, 25
	pubkey, privkey = keypair
	privkey_bytes = long_to_bytes(privkey)
	x = int(sha256(privkey_bytes).hexdigest(), 16) % 2**dbit
	while True:
		k, l = [(getRandomNBitInteger(nbit) << dbit) + x for _ in '01']
		u, v = (k * G).x(), (l * G).y()
		if u + v > 0:
			break
	h = int(sha256(msg).hexdigest(), 16)
	s = inverse(k, n) * (h * u - v * privkey) % n
	return (int(u), int(v), int(s))

def verify(msg, pubkey, sig):
	if any(x < 1 or x >= n for x in sig):
		return False
	u, v, s = sig
	h = int(sha256(msg).hexdigest(), 16)
	k, l = h * u * inverse(s, n), v * inverse(s, n)
	X = (k * G + (n - l) * pubkey).x()
	return (X - u) % n == 0

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
	pr(border, " hi all, welcome to the high secure elliptic curve signature oracle!", border)
	pr(border, " Your mission is to sign the out cryptonym, try your best :)        ", border)
	pr(border*72)

	keypair = keygen(n, G)
	pubkey, privkey = keypair

	while True:
		pr("| Options: \n|\t[P]rint the pubkey \n|\t[S]ign \n|\t[V]erify \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 'p':
			pr("| pubkey =", pubkey.x(), pubkey.y())
		elif ans == 's':
			pr("| send your hex message to sign: ")
			msg = sc()
			try:
				msg = bytes.fromhex(msg)
			except:
				die("| your message is not valid! Bye!!")
			if msg == cryptonym:
				die('| Kidding me? Bye')
			msg = msg[:14]
			sig = sign(msg, keypair)
			pr("| sign =", sig)
		elif ans == 'v':
			pr("| send your hex message to verify: ")
			msg = sc()
			try:
				msg = bytes.fromhex(msg)
			except:
				die("| your message is not valid! Bye!!")
			pr("| send the signature separated with comma: ")
			sig = sc()
			try:
				sig = [int(s) for s in sig.split(',')]
			except:
				die("| your signature is not valid! Bye!!")
			if verify(msg, pubkey, sig):
				if msg == cryptonym:
					die("| Good job! Congrats, the flag is:", FLAG)
				else:
					pr("| your message is verified!!")
			else:
				die("| your signature is not valid! Bye!!")
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()