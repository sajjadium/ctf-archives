from math import gcd
import secrets
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

n = 48

with open('flag.txt', 'rb') as f:
    flag = f.read()


def randint(a, b):
    return int(secrets.randbelow(int(b-a + 1)) + a)


def makeKey():
    W = []
    s = 0
    for i in range(n):
        curr = 0
        if i != 0:
            curr = randint((2**i - 1) * 2**n + 1, 2**(i+n))
        else:
            curr = randint(1, 2**n)
        assert s < curr
        s += curr
        W.append(curr)

    q = randint((1 << (2 * n + 1)) + 1, (1 << (2 * n + 2)) - 1)

    r = randint(2, q - 2)
    r //= gcd(r, q)

    B = []
    for w in W:
        B.append((r * w) % q)

    return B, (W, q, r)


def encrypt(public, m):
    return sum([public[i] * ((m >> (n - i - 1)) & 1) for i in range(n)])


pub, _ = makeKey()

sup_sec_num = secrets.randbits(n)

msg = encrypt(pub, sup_sec_num)

iv = secrets.token_bytes(16)

key = pad(long_to_bytes(sup_sec_num), 16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
ct = cipher.encrypt(pad(flag, 16))

print('B =', pub)
print('msg =', msg)
print('iv =', iv.hex())
print('ct =', ct.hex())
