import random
import math
from Crypto.Util.number import getPrime, bytes_to_long

with open("flag.txt", 'rb') as f:
    flag = f.read()

p = getPrime(1024)
q = getPrime(1024)
e = getPrime(8)
m = bytes_to_long(flag)
n = p * q

c = pow(m, e, n)
#change paths later
with open('enc.txt', 'w') as f:
    f.write(f'p:{p}\n')
    f.write(f'q:{q}\n')
    f.write(f'c:{c}\n')
    

print(e)