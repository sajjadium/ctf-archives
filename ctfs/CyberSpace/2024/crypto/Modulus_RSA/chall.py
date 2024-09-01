from Crypto.Util.number import bytes_to_long
from sympy import randprime

m = bytes_to_long(b'CSCTF{fake_flag}')
p, q, r = sorted([randprime(0, 1<<128) for _ in range(3)])
n = p * q * r
e = 65537
c = pow(m, e, n)
w, x, y = q % p, r % p, r % q
print(f'{w = }')
print(f'{x = }')
print(f'{y = }')
print(f'{c = }')

"""
w = 115017953136750842312826274882950615840
x = 16700949197226085826583888467555942943
y = 20681722155136911131278141581010571320
c = 2246028367836066762231325616808997113924108877001369440213213182152044731534905739635043920048066680458409222434813
"""
