from Crypto.Util.number import *
from Crypto.PublicKey import RSA


FLAG = ""
with open("flag.txt", "rb") as f:
    FLAG = f.read()

p = getPrime(2048)
p_factor = p
p *= p
q = pow(p_factor, 6)
e = 0x10001
N = p*q

"""
-
-
-
VANISHED CODE 
(known information: the cipher is just a textbook rsa)
-
-
-
"""

d = inverse(e, phi)
ciphertext = encrypt(FLAG, e, N)
exported = RSA.construct( ( N, e ) ).publickey().exportKey()

with open("key.pem", 'wb') as f:
    f.write(exported)

with open('ciphertext.txt', 'w') as f:
    f.write(ciphertext.hex())

