from Crypto.PublicKey import RSA

RSAkeys = RSA.generate(2048)
p = RSAkeys.p
q = RSAkeys.q
n = RSAkeys.n
e = RSAkeys.e
m = b"FAKE{<REDACTED>}"
c = pow(int.from_bytes(m, "big"), e, n)

mask = int("55" * 128, 16)
r = p & mask
mask = mask << 1
r += q & mask

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
print(f"r = {r}")
