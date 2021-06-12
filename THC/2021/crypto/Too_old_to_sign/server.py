#!/usr/local/bin/python3.8

from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes,bytes_to_long
from secret import FLAG, aes_key
from hashlib import sha1
from os import urandom


def sign1(sk, m):
	mq, dq = m % sk.q, sk.d % (sk.q - 1)
	mp, dp = m % sk.p, sk.d % (sk.p - 1)
	s1 = pow(mq, dp, sk.q)
	s2 = pow(mp, dp, sk.p)
	h = (sk.u * (s1 - s2)) % sk.q
	s = (s2 + h * sk.p) % sk.n
	return s

def sign2(sk, m):
	mq, dq = m % sk.q, sk.d % (sk.q - 1)
	mp, dp = m % sk.p, sk.d % (sk.p - 1)
	s1 = pow(mq, dq, sk.q)
	s2 = pow(mp, dq, sk.p)
	h = (sk.u * (s1 - s2)) % sk.q
	s = (s2 + h * sk.p) % sk.n
	return s

def pad(m,n):
	return m + urandom(n//8)

def encode(m,n):
	return b"\x6a" + m[:(n-160-16)//8] + sha1(m).digest() + b"\xbc" 


assert(len(aes_key) == 16)

private_key = RSA.generate(2048)

message = b"Here is a message to inform you that this AES key : -" + aes_key + b"- will allow you to decrypt my very secret message. I signed my message to prove my good faith, but make sure no one is watching...\n"
message += b"An anonymous vigilante trying to preserve Thcon and our delicious cassoulet"


padded_message = pad(message,2048)
encoded_message = encode(padded_message,2048)

signature1 = sign1(private_key,bytes_to_long(encoded_message))
print("signature1 =",signature1)
signature2 = sign2(private_key,bytes_to_long(encoded_message))
print("signature2 =",signature2)
print("e =",private_key.e)
print("n =",private_key.n)

pt = bytes_to_long(FLAG)
print("ct =",pow(pt,private_key.e,private_key.n))
