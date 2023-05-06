from Crypto.Util.number import getPrime
import os

flag = os.getenv("FLAG", "FakeCTF{warmup_a_frozen_cake}")
m = int(flag.encode().hex(), 16)

p = getPrime(512)
q = getPrime(512)

n = p*q

print("n =", n)
print("a =", pow(m, p, n))
print("b =", pow(m, q, n))
print("c =", pow(m, n, n))
