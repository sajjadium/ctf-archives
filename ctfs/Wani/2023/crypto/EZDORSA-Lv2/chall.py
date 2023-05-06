from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e = 7

m = b"FAKE{DUNMMY_FLAG}"

c = pow(bytes_to_long(m), e, n)
c *= pow(5, 100, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
