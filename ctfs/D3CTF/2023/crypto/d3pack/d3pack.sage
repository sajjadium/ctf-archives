from Crypto.Util.number import *
from random import *


p = getPrime(1024)
n = 50  
m = 180  

flag = b''
assert len(flag) == 48
secret = []
s = bytes_to_long(flag)
for i in range(n):
    secret.append(randint(0, p))


alpha = vector(secret)
x = [vector([randint(0, 1) for i in range(n)]) for j in range(m)]
e = vector([randint(0, p) for i in range(m)])
h = vector([(alpha * x[i] -s * e[i])% p for i in range(m)])

print("p={}\n\ne={}\n\nh={}".format(p, e, h))