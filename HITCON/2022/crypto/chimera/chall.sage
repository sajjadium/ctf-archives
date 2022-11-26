import os
from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from hashlib import sha256
from secret import flag


p = getPrime(384)
q = getPrime(384)
n = p * q
Gx = bytes_to_long(os.urandom(32))
Gy = bytes_to_long(os.urandom(32))
a = randint(1, n**2)
b = (Gy**2 - (Gx**3 + a * Gx)) % (n**2)

E = EllipticCurve(Zmod(n), [a, b])
gift = int(E.change_ring(GF(p)).order() * E.change_ring(GF(q)).order())
assert gift * E(Gx, Gy) == E(0, 1, 0)
print(f"{gift = }")

E = EllipticCurve(Zmod(n**2), [a, b])
lion_head = E(Gx, Gy)
goat_body = [randint(1, n) * lion_head for _ in range(16)]
snake_tail = [os.urandom(16) for _ in range(64)]
chimera = [sum([x * y for x, y in zip(tail, goat_body)]) for tail in snake_tail]
print("chimera =", [P.xy() for P in chimera])

key = sha256(str(sum(goat_body).xy()[0]).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_CBC, b"\0" * 16)
flagct = cipher.encrypt(pad(flag, 16))
print(f"{flagct = }")
