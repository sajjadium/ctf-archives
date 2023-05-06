from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.PublicKey import RSA
from secret import flag, getNextPrime

p = getPrime(1024)
q = getNextPrime(p)
n = p * q
e = 65537

key = RSA.construct((n, e)).export_key().decode()

with open("key", "w") as f:
    f.write(key)

m = bytes_to_long(flag.encode())
c = pow(m, e, n)
print(f"c = {c}")
