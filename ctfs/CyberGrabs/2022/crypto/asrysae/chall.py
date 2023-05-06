from Crypto.Util.number import *
import gmpy2
from secret import flag
import binascii

p = getPrime(512)
q = getPrime(512)
e = 65537

m = bytes_to_long(flag)

ciphertext = pow(m, e, p*q)

ciphertext = long_to_bytes(ciphertext)
obj1 = open("ciphertext.txt",'w')
obj1.write(f"p={p}\n\n")
obj1.write(f"q={q}\n\n")
obj1.write(f"ct={ciphertext.hex()}")