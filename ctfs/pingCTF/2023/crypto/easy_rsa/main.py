from Crypto.Util.number import getPrime
from Crypto.Util.number import bytes_to_long

p = getPrime(2048)
q = getPrime(2048)
n = p * q
e = 65537
d = pow(e, -1, (p-1)*(q-1))
flag = open("flag.txt","rb").read()

print(f"q & p = {q & p}")
print(f"q & (p << 1) = {q & (p << 1)}")
print(f"n = {n}")
print(f"ct = {pow(bytes_to_long(flag), e, n)}")
