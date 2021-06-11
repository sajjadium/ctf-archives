#!/usr/bin/env sage

from flag import flag

def make_matrix(n):
	Zn = IntegerModRing(n)
	G = GL(2, Zn)
	while True:
		a, b, c, d = [randint(0, n - 1) for _ in range(4)]
		P = G([[a, b], [c, d]])
		if P in G:
			return P

def bpow(P, n):
	if n == 0:
		return P
	for _ in range(n):
		P = P ** 2
	return P

def make_keypair(n):
	Zn = IntegerModRing(n)
	G = GL(2, Zn)
	I = G([[1, 0], [0, 1]])
	r = randint(1, 2 ** 256)
	br = bin(r)[2:][::-1]
	J = I
	while True:
		P, Q = [make_matrix(n) for _ in range(2)]
		try:	
			if Q * (~P) != P * Q:
				for i in range(len(br)):
					if br[i] == '1':
						J = bpow(Q, i) * J
				B = (~Q) * (~P) * Q
				pubkey = (n, P, B, J)
				privkey = Q
				return (pubkey, privkey)
		except:
			continue

def encrypt(m, pubkey):
	n, P, B, J = pubkey
	Zn = IntegerModRing(n)
	G = GL(2, Zn)
	I = G([[1, 0], [0, 1]])
	s = randint(1, 2 ** 32)
	bs = bin(s)[2:][::-1]
	D = I
	for i in range(len(bs)):
		if bs[i] == '1':
			D = bpow(J, i) * D
	E = (~D) * P * D
	K = (~D) * B * D
	l = len(str(m))
	M = []
	for i in range(0, 4):
		M.append(int(str(m)[i*l // 4: (i+1)*l // 4]))
	U = matrix([[M[1], M[0]], [M[3], M[2]]])
	V = K * U * K
	return (V, E)

p = next_prime(randint(1, 2 ** 72))
q = next_prime(randint(1, 2 ** 72))

n = p * q
pubkey, privkey = make_keypair(n)

flag = flag.encode('utf-8')
m = int(flag.hex(), 16)
enc = encrypt(m, pubkey)

print('pubkey = ', pubkey)
print('enc = ', enc)