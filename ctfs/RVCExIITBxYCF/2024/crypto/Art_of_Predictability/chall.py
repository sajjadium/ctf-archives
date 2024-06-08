from Crypto.Util.number import bytes_to_long, isPrime
from secrets import randbelow
from sympy import nextprime

s = 696969
p = bytes_to_long(REDACTED)

c = 0
while not isPrime(p):
    p+=1
    c+=1

assert isPrime(p)

a = randbelow(p)
b = randbelow(p)

def mathemagic(seed):
    return (a * seed + b) % p

print("c = ", c)
print("a = ", a)
print("b = ", b)
print("mathemagic(seed) = ", mathemagic(s))
print("mathemagic(mathemagic(seed)) = ", mathemagic(mathemagic(s)))