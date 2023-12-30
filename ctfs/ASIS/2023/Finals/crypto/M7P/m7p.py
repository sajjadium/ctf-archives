#!/usr/bin/env python3

import os
from hashlib import *
from binascii import *
from Crypto.Cipher import AES
from Crypto.Util.number import *
from flag import flag

def next_prime(n):
	while True:
		if isPrime(n):
			return n
		n += 1

def find(s, ch):
	return [i for i, ltr in enumerate(ch) if ltr == s]

def worth(c, msg):
	assert len(c) == 1
	w = 0
	if c in msg:
		a = find(c, msg)
		w += sum([(_ + 1)**_ - _ for _ in a])
	return w

def xor(mm, ym):
	xm = []
	for i in range(len(mm)):
		xm.append(mm[i] ^ ym[i])
	return bytes(xm)

def taft(key, otp):
	assert len(key) == len(otp)
	T = []
	for _ in range(len(key)):
		__ = xor(key, otp)
		T.append(hexlify(__))
		otp = sha1(otp).hexdigest().encode()
	return T

def gaz(T):
	G = []
	for t in T:
		R = []
		for c in range(16):
			R.append(worth(hex(c)[2:], t.decode()))
		p = next_prime(sum(R))
		a = getPrime(p.bit_length() >> 3)
		R = [r * a % p for r in R]
		G.append(R)
	return G

def lili(gz, s):
	i, L = 0, []
	for g in gz:
		s_i = bin(bytes_to_long(s[2*i:2*i + 2]))[2:].zfill(16)
		L.append(sum([g[_] * int(s_i[_]) for _ in range(16)]))
		i += 1
	return L

def encrypt(msg, key):
	cipher = AES.new(key, AES.MODE_GCM)
	enc, tag = cipher.encrypt_and_digest(msg)
	return (enc, cipher.nonce, tag)

some = os.urandom(40)
good = os.urandom(40)
keys = os.urandom(80)

T = taft(some, good)
G = gaz(T)
L = lili(G, keys)

mask = xor(flag, sha512(keys).digest()[:len(flag)])
enc = encrypt(mask, sha256(some).digest())

print(f'G = {G}')
print(f'L = {L}')
print("c = ", *enc, sep = "")