#! /usr/bin/env python3
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes


key = RSA.generate(4096, e = 5)
msg = b"Congrats! Your flag is: OFPPT-CTF{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}."
m = bytes_to_long(msg)
print("e = ".format(key.e))
print("n = ".format(key.n))
c = pow(m, key.e, key.n)
print("c = ".format(c))


