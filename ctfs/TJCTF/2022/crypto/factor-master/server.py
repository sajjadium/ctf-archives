#!/usr/local/bin/python -u

from Crypto.Util.number import getPrime, isPrime, getRandomInteger
import sys, random

print("Are you truly the master here?")
print()
print("We'll have to find out...")
print()

def fail():
    print("You are not the master!")
    sys.exit(1)

def challenge1():
    p = getPrime(44)
    q = getPrime(1024)
    n = p * q
    return [p, q], n

def challenge2():
    p = getPrime(1024)
    q = p + getRandomInteger(524)
    if q % 2 == 0: q += 1
    while not isPrime(q): q += 2
    n = p * q
    return [p, q], n

def challenge3():
    small_primes = [n for n in range(2,10000) if isPrime(n)]
    def gen_smooth(N):
        r = 2
        while True:
            p = random.choice(small_primes)
            if (r * p).bit_length() > N:
                return r
            r *= p
    p = 1
    while not isPrime(p):
        p = gen_smooth(1024) + 1
    q = getPrime(1024)
    n = p * q
    return [p, q], n

challenges = [challenge1, challenge2, challenge3]
responses = ["Okay, not bad.", "Nice job.", "Wow."]

for i, chal in enumerate(challenges):
    print(f"CHALLENGE {i+1}")
    factors, n = chal()
    factors.sort()
    print(f"n = {n}")
    guess = input("factors = ? ")
    if guess != " ".join(map(str,factors)):
        fail()
    print(responses[i])
    print()

print("Here's your flag:")
with open("flag.txt") as f:
    print(f.read().strip())
