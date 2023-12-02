from Crypto.Util.number import *

p = getPrime(512)
q = getPrime(512)

n = p*q
e = 65537

m = bytes_to_long(b"nbctf{[REDACTED]}")

ct = pow(m,e,n)

print(f"{ct = }")
print(f"{e = }")
print(f"{n = }")

hint = (p+q) >> 200 # I can't be giving you that much!
print(f"{hint = }")
