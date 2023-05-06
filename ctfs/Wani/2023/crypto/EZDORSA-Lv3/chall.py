from Crypto.Util.number import *

e = 65537

n = 1
prime_list = []
while len(prime_list) < 100:
    p = getPrime(25)
    if not (p in prime_list):
        prime_list.append(p)

for i in prime_list:
    n *= i

m = b"FAKE{DUMMY_FLAG}"
c = pow(bytes_to_long(m), e, n)

print(f"n = {n}")
print(f"e = {e}")
print(f"c = {c}")
