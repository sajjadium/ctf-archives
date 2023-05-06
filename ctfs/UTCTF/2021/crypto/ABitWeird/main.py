from Crypto.Util import number
from secret import flag
import os

length = 2048
p, q = number.getPrime(length//2), number.getPrime(length//2)
N = p*q
e = 3

m = number.bytes_to_long(flag)
x = number.bytes_to_long(os.urandom(length//8))

c = pow(m|x, e, N)
print('N =', N);
print('e =', e);
print('c =', c);
print('m&x =', m&x);
