import Crypto.Util.number as cun
import math

message = b"bctf{fake_flag}"

m = int.from_bytes(message, "big")

p = cun.getPrime(128)
q = cun.getPrime(128)
e = 65537

n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
assert (e * d) % phi == 1
assert math.gcd(e, phi) == 1

c = pow(m, e, n)

print(f"e = {e}")
print(f"n = {n}")
print(f"c = {c}")

"""
Output:
e = 65537
n = 66082519841206442253261420880518905643648844231755824847819839195516869801231
c = 19146395818313260878394498164948015155839880044374872805448779372117637653026
"""
