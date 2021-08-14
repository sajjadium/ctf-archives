#!/usr/bin/python3

from random import getrandbits as rand
from gmpy2 import next_prime, invert
import pickle

FLAG = open('flag.txt', 'rb').read()
BUF = 16

def encrypt(msg, key):
	msg = format(int(msg.hex(), 16), f'0{len(msg)*8}b')[::-1]
	assert len(msg) == len(key)
	return sum([k if m=='1' else 0 for m, k in zip(msg, key)])

def decrypt(ct, pv):
	b, r, q = pv
	ct = (invert(r, q)*ct)%q
	msg = ''
	for i in b[::-1]:
		if ct >= i:
			msg += '1'
			ct -= i
		else:
			msg += '0'
	return bytes.fromhex(hex(int(msg, 2))[2:])

def gen_inc_list(size, tmp=5):
	b = [next_prime(tmp+rand(BUF))]
	while len(b)!=size:
		val = rand(BUF)
		while tmp<sum(b)+val:
			tmp = next_prime(tmp<<1)
		b += [tmp]
	return list(map(int, b))

def gen_key(size):
	b = gen_inc_list(size)
	q = b[-1]
	for i in range(rand(BUF//2)):
		q = int(next_prime(q<<1))
	r = b[-1]+rand(BUF<<3)
	pb = [(r*i)%q for i in b]
	return (b, r, q), pb

if __name__ == '__main__':
    pvkey, pbkey = gen_key(len(FLAG) * 8)
    cip = encrypt(FLAG, pbkey)
    assert FLAG == decrypt(cip, pvkey)
    pickle.dump({'cip': cip, 'pbkey': pbkey}, open('enc.pickle', 'wb'))
