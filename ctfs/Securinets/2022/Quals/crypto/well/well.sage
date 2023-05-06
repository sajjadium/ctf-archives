import random, hashlib, os, sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

FLAG = b"Securinets{REDACTED}"

def gen_key(P, Q):
    seed = P.weil_pairing(Q, P.order())
    return hashlib.sha256(str(seed).encode()).digest()[:16]

e1, e2 = 19, 61
l1, l2 = 2, 3
p = l1^e1*l2^e2 - 1
_.<x> = PolynomialRing(GF(p))
Q.<i> = GF(p^2, modulus=x^2 + 1)

E = EllipticCurve(Q, [1, 0])
assert E.is_supersingular()

K = E(0)
while (l1^(e1-1))*K == 0:
	K = l2^e2 * E.random_point()
φ = E.isogeny(K)

while True:
	G1 = E.random_point()
	G2 = E.random_point()
	φ_G1 = φ(G1)
	φ_G2 = φ(G2)
	if φ_G1.order() == φ_G2.order():
		break

key = gen_key(φ_G1, φ_G2)
iv = os.urandom(16)
aes = AES.new(key, AES.MODE_CBC, iv)
encrypted_flag = aes.encrypt(pad(FLAG, 16))

print(f"G1 : {G1.xy()}")
print(f"G2 : {G2.xy()}")
print(f"Encrypted flag : {(iv + encrypted_flag).hex()}")