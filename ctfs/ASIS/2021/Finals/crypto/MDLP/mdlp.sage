#!/usr/bin/env sage

from sage.all import *
from Crypto.Util.number import *
from secret import gen_prime, gen_base_matrix, flag

def keygen(nbit, l):
	#
	## Create the n-bit prime and base square matrix of size l over Ring Z_p
	#
	p = gen_prime(nbit)
	A = gen_base_matrix(p, l)

	d = randint(2, p)
	Q = A ** d
	pubkey = (p, A, Q)
	privkey = d
	return pubkey, privkey

def encrypt(M, pubkey):
	p, A, Q = pubkey
	l = A.nrows()
	assert M.nrows() == l
	r = randint(2, p)
	C, D = A ** r, Q ** r
	E = D * M
	return C, E

def msg_to_matrix(p, msg):
	l = len(msg)
	return matrix(Zmod(p), [[bytes_to_long(msg[0:l//4]), bytes_to_long(msg[l//4:l//2])], 
			[bytes_to_long(msg[l//2:3*l//4]), bytes_to_long(msg[3*l//4:l])]])

nbit, l = 256, 2
pubkey, privkey = keygen(nbit, l)
p, A, Q = pubkey
M = msg_to_matrix(p, flag)
ENC = encrypt(M, pubkey)

print(f'pubkey = {pubkey}')
print(f'ENC = {ENC}')
