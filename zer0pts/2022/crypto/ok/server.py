from Crypto.Util.number import isPrime, getPrime, getRandomRange, inverse
import os
import signal

signal.alarm(300)

flag = os.environ.get("FLAG", "0nepoint{GOLDEN SMILE & SILVER TEARS}")
flag = int(flag.encode().hex(), 16)

P = 2 ** 1000 - 1
while not isPrime(P): P -= 2

p = getPrime(512)
q = getPrime(512)
e = 65537
phi = (p-1)*(q-1)
d = inverse(e, phi)
n = p*q

key = getRandomRange(0, n)
ciphertext = pow(flag, e, P) ^ key

x1 = getRandomRange(0, n)
x2 = getRandomRange(0, n)

print("P = {}".format(P))
print("n = {}".format(n))
print("e = {}".format(e))
print("x1 = {}".format(x1))
print("x2 = {}".format(x2))

# pick a random number k and compute v = k**e + (x1|x2)
# if you add x1, you can get key = c1 - k mod n
# elif you add x2, you can get ciphertext = c2 - k mod n
v = int(input("v: "))

k1 = pow(v - x1, d, n)
k2 = pow(v - x2, d, n)

print("c1 = {}".format((k1 + key) % n))
print("c2 = {}".format((k2 + ciphertext) % n))
