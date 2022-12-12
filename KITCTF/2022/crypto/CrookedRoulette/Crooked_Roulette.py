#!/usr/bin/env python3
from math import gcd
from Crypto.Util.number import getPrime,getRandomInteger

flag = "KITCTF{fake_flag}"

p = getPrime(512)
q = getPrime(512)
n = p*q
phi = (p-1)*(q-1)
e = getPrime(256)
while gcd(e, phi) != 1:
    e = getPrime(256)

d = pow(e, -1, phi)

def sign(m):
    return pow(m, d, n)

def check(c, m):
    return pow(c, e, n) == m

result = getRandomInteger(256)
print(f"Number of pockets: {hex(n)}")
print(f"The Manager told me, the roulette is crooked and will hit {hex(result)}")
base = 16
m2 = int(input(f"What should I bet? "), base)
if m2 % n == result:
    print("It is too obvious if I bet that")
else:
    s2 = sign(m2)
    print(f"My Signatur is {hex(s2)}")
    message = int(input(f"What do you want to bet? "), base)
    signature = int(input(f"Please sign your bet "), base)
    if result == message and check(signature, message):
        print(f"You Win: {flag}")
    else:
        print("You Lose")
    
