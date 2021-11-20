from Crypto.Util.number import *
import random
from secret import flag

def gettoken(c):
    X = 0
    while ((pow(X, (p-1)//2, p)!=1) or (pow(X, (q-1)//2, q)!=1)):
        X = 1
        while X.bit_length() < 920:
            X *= random.choice(primes)
    xp = pow(X, (p + 1)//4, p)
    xq = pow(X, (q + 1)//4, q)
    xp = random.choice([xp,-xp%p])
    xq = random.choice([xq,-xq%q])
    x = c * (xp*inverse(q,p)*q + xq*inverse(p,q)*p) % n
    return x

def getmyPrime(nbits):
    p = getPrime(nbits)
    while(p%4==1):
        p = getPrime(nbits)
    return p

primes = random.sample(sieve_base, 920)
p = getmyPrime(512)
q = getmyPrime(512)
e = 65537
n = p*q
c = pow(bytes_to_long(flag), e, n)

with open("output.txt", "w")as f:
    f.write("n = " + str(n) + "\n")
    for i in range(920):
        f.write("Token #"+str(i+1)+': '+str(gettoken(c))+'\n')
