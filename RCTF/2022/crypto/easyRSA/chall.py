from Crypto.Util.number import getPrime, inverse, bytes_to_long

with open('flag.txt', 'rb') as f:
    flag = f.read()


def v(k):
    if k == 0:
        return 2
    if k == 1:
        return r
    return (r * v(k - 1) - v(k - 2)) % (N * N)


def encrypt(m, e, N):
    c = (1 + m * N) * v(e) % (N * N)
    return c


p = getPrime(512)
q = getPrime(512)
N = p * q
d = getPrime(512)
r = getPrime(512)
e = inverse(d, (p * p - 1) * (q * q - 1))
c = encrypt(bytes_to_long(flag), e, N)
print(f"e = {e}")
print(f"c = {c}")
print(f"N = {N}")
