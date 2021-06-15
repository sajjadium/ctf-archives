from Crypto.Util.number import *
import binascii
flag = open('flag.txt','rb').read()
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 2**16+1
pt = int(binascii.hexlify(flag).decode(),16)
print(p>>512)
print(q%(2**512))
print(n, e)
print(pow(pt,e,n))
