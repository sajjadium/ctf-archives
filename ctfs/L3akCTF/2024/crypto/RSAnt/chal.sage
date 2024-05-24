from random import *
from sage.all import *
from Crypto.Util.number import *
from secret import flag

def encrypt():
    tmp = randint(2**1023, 2**1024)
    p = next_prime(1337*tmp + randint(2, 2**512))
    q = next_prime(7331*tmp + randint(2, 2**512))
    N = p*q
    return N

def l3ak(n):
    print('Security Alert!!')
    print('There is a L3AKER l3aking our data!! [~] :/\n')
    c1 = pow(bytes_to_long(b"factoring modulus?"), e, n)
    c2 = pow(bytes_to_long(b"without the modulus?"), e, n)
    return c1, c2

e = 65537
n = encrypt()
enc = pow(flag, e, n)
c1, c2 = l3ak(n)

print(f'Encrypted flag = {enc}\n')
print(f'c1 = {c1}\n')
print(f'c2 = {c2}\n')
