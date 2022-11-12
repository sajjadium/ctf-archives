from Crypto.Util.number import *
from Crypto.Random import *
from flag import flag

p = getPrime(512)
q = getPrime(512)
r = getPrime(512)
n = p * q * r
e = 2 * 65537

assert n.bit_length() // 8 - len(flag) > 0
padding = get_random_bytes(n.bit_length() // 8 - len(flag))
m = bytes_to_long(padding + flag)

assert m < n

c1p = pow(p, e, n)
c1q = pow(q, e, n)
cm = pow(m, e, n)
c1 = (c1p - c1q) % n
c2 = pow(p - q, e, n)

print(f"e = {e}")
print(f"n = {n}")
# p^e - q^e mod n
print(f"c1 = {c1}")
# (p-q)^e mod n
print(f"c2 = {c2}")
# m^e mod n
print(f"cm = {cm}")
