from Crypto.Util.number import *
def myGetPrime():
    while True:
        x = getRandomNBitInteger(1024) & ((1 << 1024) - 1)//3
        if isPrime(x):
            return x
p = myGetPrime()
q = myGetPrime()
n = p * q
e = 65537
message = open('flag.txt', 'rb')
m = bytes_to_long(message.read())
c = pow(m, e, n)
open("superstitious-2.txt", "w").write(f"n = {n}\ne = {e}\nc = {c}")
