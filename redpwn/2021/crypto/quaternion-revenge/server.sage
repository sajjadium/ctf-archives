#!/usr/bin/env sage
from Crypto.Util.number import getPrime, bytes_to_long
import secrets

with open('flag.txt','r') as flagfile:
    flag = flagfile.read().strip()

with open('secret.txt','rb') as secret:
    M = secret.read().strip()
m = bytes_to_long(M)

p = getPrime(512)
q = getPrime(512)
n = p * q
e = 65537
Q.<i,j,k> = QuaternionAlgebra(-p,-q)

#randomize M per-instance
m ^^= secrets.randbelow(n)

#prepare leaks
n  = n
l  = m.bit_length()
c1 = pow(m,e,p)
c2 = pow(m,e,q)

#reveal leaks
print('n:',n)
print('l:',l)
print('c1:',c1)
print('c2:',c2)

#Present challenge
try:
    print("Calculate the left quaternion isomorphism of m:")
    inp = input('>>> ').strip()
    assert all([x in '1234567890 ijk*+' for x in inp])
    if eval(inp)==m:
        print(flag)
    else:
        print('Wrong!')
except AssertionError:
    print("Invalid characters.")
except Exception:
    print("Error.")
