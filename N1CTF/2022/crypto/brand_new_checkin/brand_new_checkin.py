from Crypto.Util.number import *
from random import getrandbits
from secret import flag

def keygen():
    p = getPrime(512)
    q = getPrime(512)

    n = p * q
    phi = (p-1)*(q-1)

    while True:
        a = getrandbits(1024)
        b = phi + 1 - a

        s = getrandbits(1024)
        t = -s*a * inverse(b, phi) % phi

        if GCD(b, phi) == 1:
            break
    return (s, t, n), (a, b, n)


def enc(m, k):
    s, t, n = k
    r = getrandbits(1024)

    return m * pow(r, s, n) % n, m * pow(r, t, n) % n


pubkey, privkey = keygen()

flag = pow(bytes_to_long(flag), 0x10001, pubkey[2])

c = []
for m in long_to_bytes(flag):
    c1, c2 = enc(m, pubkey)
    c.append((c1, c2))

print(pubkey)
print(c)

