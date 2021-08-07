from Crypto.Util.number import *

p = getPrime(256)
q = getPrime(256)
n = p * q
e = 0x69420

flag = bytes_to_long(open("flag.txt", "rb").read())
print("n =",n)
print("e =", e)
print("ct =",(flag * e) % n)
