from secret import e,msg
from Crypto.Util.number import*
from gmpy2 import *
from Crypto.PublicKey import RSA

p = getPrime(2048)
q = getPrime(2048)
n = p*q
m = bytes_to_long(msg)
ct = pow(m,e,n)
with open("ciphertext.txt", "w") as f:
    f.write(ct)
key = RSA.construct((int(n), int(e), int(d), int(p), int(q)))
pem = key.export_key('PEM')
with open("private_key.pem", "wb") as f:
    f.write(pem)