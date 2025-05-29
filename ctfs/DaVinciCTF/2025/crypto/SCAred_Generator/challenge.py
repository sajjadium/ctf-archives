from hidden import FLAG
from Crypto.Util.number import bytes_to_long, getRandomInteger, isPrime
import sympy

def getPrime(b=512):
    v = 2 * getRandomInteger(b) + 1  # Random odd number
    while 1:
        v += 2
        R = sympy.sieve.primerange(1000)
        for r in R:
            if v % r == 0:  # Trial division
                print("Ahh ! My test failed on", r)
                break
        else:
            if isPrime(v): return v
            print("Oh nooo ! isPrime test failed")

n = getPrime() * getPrime()  # RSA modulus
ct = pow(bytes_to_long(FLAG), 65537, n)  # RSA encryption

print(f"{n=}")
print(f"{ct=}")  # Encrypted flag
