from Crypto.Util.number import *
from secret import FLAG

BITS = 1024
p = random_prime(2**BITS)
q = random_prime(2**BITS)
n = p*q
psi = (p**2 + p + 1) * (q**2 + q + 1)
delta = 0.3

while True:
    d = randint(0, int(n**delta))
    if gcd(d, psi) == 1:
        break
e = pow(d, -1, psi)

assert gcd(e,p-1) == 1 and gcd(e,q-1) == 1

print(f'e = {e}')

m = bytes_to_long(FLAG)
ct = pow(m,e,n)

prec = 3*(BITS + BITS//4) + 1
a , b = getRandomInteger(312) , getRandomInteger(312)
c , d = getRandomInteger(312) , getRandomInteger(312)
while(true):
    h1 = ZZ(a*p + b*q)
    h2 = ZZ(c*p + d*q)
    h3 = (h1/h2).n(prec)
    g = (gcd(h1 , h2))
    if (g == 1):
        break
#h3.dump('hint.sobj')
print(f'hint = {h3}')
