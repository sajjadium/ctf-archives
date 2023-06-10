from Crypto.Util.number import *
import math
def myGetPrime():
    while True:
        x = getRandomNBitInteger(1024)
        for i in range(-10,11):
            if isPrime(x*x+i):
                return x*x+i
p = myGetPrime()
q = myGetPrime()
n = p * q
e = 65537
message = open('flag.txt', 'rb')
m = bytes_to_long(message.read())
c = pow(m, e, n)
open("superstitious.txt", "w").write(f"n = {n}\ne = {e}\nc = {c}")