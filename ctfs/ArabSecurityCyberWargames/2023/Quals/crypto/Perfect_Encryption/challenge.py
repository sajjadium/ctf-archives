from Crypto.Util.number import bytes_to_long, getStrongPrime
from random import getrandbits

FLAG = bytes_to_long(b"ASCWG{XXXX}")

p = getStrongPrime(512)
a, b, c = getrandbits(256), getrandbits(256), getrandbits(256)

x = getrandbits(512)
y = FLAG*x % p

f1 = (a*x*y + b*x - c*y + a*b) % p
f2 = (a*x*y - a*b*x + c*y - a*b*c) % p
f3 = (a*x*y + a*b*x - b*y + a*c) % p

print(f"{a=}\n{b=}\n{c=}\n{p=}")
print(f"{f1=}\n{f2=}\n{f3=}")



