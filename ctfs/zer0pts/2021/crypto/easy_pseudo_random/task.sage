from Crypto.Util.number import*
from flag import flag

nbits = 256
p = random_prime(1 << nbits)
Fp = Zmod(p)
P.<v> = PolynomialRing(Fp)

b = randrange(p)
d = 2
F = v^2 + b

v0 = randrange(p)
v1 = F(v0)

k = ceil(nbits * (d / (d + 1)))
w0 = (v0 >> (nbits - k))
w1 = (v1 >> (nbits - k))

# encrypt
m = bytes_to_long(flag)
v = v1
for i in range(5):
    v = F(v)
    m ^^= int(v)

print(f"p = {p}")
print(f"b = {b}")
print(f"m = {m}")
print(f"w0 = {w0}")
print(f"w1 = {w1}")
