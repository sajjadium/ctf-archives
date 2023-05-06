mport binascii
import random
from Crypto.Util.number import isPrime

flag = open("flag.txt", "rb").read().strip()
m = int(binascii.hexlify(flag), 16)

def genPrimes(size):
    base = random.getrandbits(size // 2) << size // 2
    base = base | (1 << 1023) | (1 << 1022) | 1
    while True:
        temp = base | random.getrandbits(size // 2)
        if isPrime(temp):
            p = temp
            break
    while True:
        temp = base | random.getrandbits(size // 2)
        if isPrime(temp):
            q = temp
            break
    return (p, q)

p, q = genPrimes(1024)
n = p * q
e = 0x10001

print("c:", pow(m, e, n))
