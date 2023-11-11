from Crypto.Util.number import getPrime, getRandomRange, inverse, GCD
import os

flag = os.getenv("FLAG", "FakeCTF{sushi_no_ue_nimo_sunshine}").encode()


def keygen():
    p = getPrime(512)
    q = getPrime(512)

    n = p * q
    phi = (p-1)*(q-1)

    while True:
        a = getRandomRange(0, phi)
        b = phi + 1 - a

        s = getRandomRange(0, phi)
        t = -s*a * inverse(b, phi) % phi

        if GCD(b, phi) == 1:
            break
    return (s, t, n), (a, b, n)


def enc(m, k):
    s, t, n = k
    r = getRandomRange(0, n)

    c1, c2 = m * pow(r, s, n) % n, m * pow(r, t, n) % n
    assert (c1 * inverse(m, n) % n) * inverse(c2 * inverse(m, n) % n, n) % n == pow(r, s - t, n)
    assert pow(r, s -t ,n) == c1 * inverse(c2, n) % n
    return m * pow(r, s, n) % n, m * pow(r, t, n) % n


def dec(c1, c2, k):
    a, b, n = k
    return pow(c1, a, n) * pow(c2, b, n) % n


pubkey, privkey = keygen()

c = []
for m in flag:
    c1, c2 = enc(m, pubkey)
    assert dec(c1, c2, privkey)

    c.append((c1, c2))

print(pubkey)
print(c)

