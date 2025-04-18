from Crypto.Util import number

flag = b"UMASS{REDACTED}"
bits = 1024

p = number.getPrime(bits)
q = number.getPrime(bits)

n = p * q
phi = (p - 1) * (q - 1)
e = 65537
d = number.inverse(e, phi)

c = pow(int.from_bytes(flag, 'big'), e, n)
print(f"n: {n}")
print(f"e: {e}")
print(f"c: {c}")
print(f"partial p^q: {hex((p^q) >> (bits // 2))}")
