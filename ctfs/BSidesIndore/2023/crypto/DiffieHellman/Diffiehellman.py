from Crypto.Util.number import *
from secrets import randbelow

flag = b'BSidesIndore{?????????????????????????????????????????}'


p = getPrime(1024)
a = randbelow(p)
b = randbelow(p)
s = randbelow(p)

#private_key
na = randbelow(p)
nb = randbelow(p)

def f(z):
    return (a * z + b) % p

def compose_f(z , n):
    for _ in range(n):
        z = f(z)
    return z



#public_key
A = compose_f(s, na)
B = compose_f(s, nb)

shared_secret = compose_f(A, nb)
assert compose_f(B, na) == shared_secret

m = bytes_to_long(flag)
hint = (shared_secret * m) % p


print('p=' , p)
print('a=' , a)
print('b=' , b)
print('s=', s)
print('A=' , A)
print('B=' , B)
print('Hint=' , hint)