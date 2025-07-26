#!/usr/local/bin/python
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

print('Yo welcome to my sign as a service...')

p, q = getPrime(512), getPrime(512)
e = 12389231641983877009741841713701317189420787527171545487350619433744301520682298136425919859970313849150196317044388637723151690904279767516595936892361663
n = p * q
d = pow(e, -1, (p - 1) * (q - 1))

k = get_random_bytes(16)
cipher = AES.new(k, AES.MODE_ECB)

flag = open('flag.txt', 'rb').read()
assert len(flag) <= 50
ct = pow(bytes_to_long(flag), e, n)

print(ct)

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print(cipher.encrypt(pad(long_to_bytes(pow(i, d, n) & ((1<<512) - 1)), 16)).hex())
	except:
		print("bad input, exiting")