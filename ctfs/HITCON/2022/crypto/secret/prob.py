import random, os
from Crypto.Util.number import getPrime, bytes_to_long

p = getPrime(1024)
q = getPrime(1024)
n = p * q

flag = open('flag','rb').read()
pad_length = 256 - len(flag)
m = bytes_to_long(os.urandom(pad_length) + flag)
assert(m < n)
es = [random.randint(1, 2**512) for _ in range(64)]
cs = [pow(m, p + e, n) for e in es]
print(es)
print(cs)
