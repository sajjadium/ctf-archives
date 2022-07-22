#!/usr/local/bin/python

import re
from Crypto.Util.number import isPrime, GCD

flag_regex = rb"hope{[a-zA-Z0-9_\-]+}"

with open("ciphertext.txt", "r") as f:
	c = int(f.read(), 10)

print(f"Welcome to reverse RSA! The encrypted flag is {c}.  Please provide the private key.")

p = int(input("p: "), 10)
q = int(input("q: "), 10)
e = int(input("e: "), 10)

N = p * q
phi = (p-1) * (q-1)

if (p < 3) or not isPrime(p) or (q < 3) or not isPrime(q) or (e < 2) or (e > phi) or GCD(p,q) > 1 or GCD(e, phi) != 1:
	print("Invalid private key")
	exit()


d = pow(e, -1, phi)
m = pow(c, d, N)

m = int.to_bytes(m, 256, 'little')
m = m.strip(b"\x00")

if re.fullmatch(flag_regex, m) is not None:
	print("Clearly, you must already know the flag!")

	with open('flag.txt','rb') as f:
		flag = f.read()
		print(flag.decode())

else:
	print("hack harder")
