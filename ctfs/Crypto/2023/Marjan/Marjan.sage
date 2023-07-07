#!/usr/bin/env sage

import sys
from Crypto.Util.number import *
from hashlib import sha256
from flag import flag


p = 114863632180633827211184132915225798242263961691870412740605315763112513729991
A = -3
B = 105675527217961035404524512435875047840495516468907806313576241823653895562912
E = EllipticCurve(GF(p), [A, B])
G = E.random_point()
_o = E.order()
original_msg = 'I love all cryptographers!!!'

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.buffer.readline()

def keygen(E):
	skey = randint(1, _o)
	pkey = skey * G
	return pkey, skey

def encrypt(msg, pkey):
	e, l = randint(1, _o), len(msg)
	m1, m2 = bytes_to_long(msg[:l // 2]), bytes_to_long(msg[l // 2:])
	assert m1 < p and m2 < p
	e1, e2 = (e * pkey).xy()
	c1, c2 = m1 * e1 % p, m2 * e2 % p
	return (c1, c2, e * G)

def sign(msg, skey):
	_tail = bytes_to_long(sha256(str(skey).encode('utf-8')).digest()) % (1 << 24)
	while True:
		K = [randint(1, 2**255) // (1 << 24) + _tail for _ in '__']
		r, s = int((K[0] * G).xy()[0]), int((K[1] * G).xy()[1])
		if r * s != 0:
			break
	h = bytes_to_long(sha256(msg).digest())
	t = inverse(K[0], _o) * (h * r - s * skey) % _o
	return (r, s, t)

def verify(msg, pkey, _sign):
	r, s, t = [int(_) % _o for _ in _sign]
	h = bytes_to_long(sha256(msg.encode('utf-8')).digest())
	u = h * r * inverse(t, _o) % _o
	v = s * inverse(t, _o) % _o
	_R = (u * G - v * pkey).xy()[0]
	return _R == r

def main():
	border = "|"
	pr(border*72)
	pr(border, "Hi all, now it's time to solve a probably simple ECC challenge about", border)
	pr(border, "encryption and signing in elliptic curves! Follow the questions and ", border)
	pr(border, "find the secret flag, are you ready!?                               ", border)
	pr(border*72)

	pkey, skey = keygen(E)

	while True:
		pr("| Options: \n|\t[E]ncrypt a message! \n|\t[G]et the flag \n|\t[P]ublic Key \n|\t[S]ign a message \n|\t[V]erify signature \n|\t[Q]uit")
		ans = sc().decode().lower().strip()
		if ans == 'e':
			pr(border, 'Send your message here: ')
			_msg = sc()
			_enc = encrypt(_msg, pkey)
			pr(border, f'enc = {_enc}')
		elif ans == 'g':
			pr(border, 'You should send the valid signature for my given message!')
			pr(border, 'Send the signature of original message here: ')
			_sgn = sc().split(b',')
			_sgn = [int(_) for _ in _sgn]
			try:
				_sgn = [int(_) for _ in _sgn]
				if verify(original_msg, pkey, _sgn):
					die(border, f'Congratz! You got the flag: {flag}')
				else:
					pr(border, 'Your signature is not correct!')
			except:
				pr(border, 'Try to send valid signature!')
				continue
		elif ans == 's':
			pr(border, 'Send your message to sign: ')
			_msg = sc()
			if len(_msg) >= 10:
				die(border, 'Sorry, I sign only short messages! :/')
			_sgn = sign(_msg, skey)
			pr(border, f'sgn = {_sgn}')
		elif ans == 'v':
			pr(border, 'Send your signature to verify: ')
			_sgn = sc().split(b',')
			try:
				_sgn = [int(_) for _ in _sgn]
				pr(border, 'Send your message: ')
				_msg = sc()
				if verify(_msg, pkey, _sgn):
					pr(border, 'Your message successfully verified :)')
				else:
					pr(border, 'Verification failed :(')
			except:
				pr(border, 'Try to send valid signature!')
				continue
		elif ans == 'p':
			pr(border, f'pkey = {pkey}')
			pr(border, f'G = {G}')
		elif ans == 'q':
			die(border, 'Quitting...')
		else:
			die(border, 'You should select valid choice!')

if __name__ == '__main__':
	main()