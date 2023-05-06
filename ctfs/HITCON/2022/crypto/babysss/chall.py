from random import SystemRandom
from Crypto.Cipher import AES
from hashlib import sha256
from secret import flag

rand = SystemRandom()


def polyeval(poly, x):
    return sum([a * x**i for i, a in enumerate(poly)])


DEGREE = 128
SHARES_FOR_YOU = 8  # I am really stingy :)

poly = [rand.getrandbits(64) for _ in range(DEGREE + 1)]
shares = []
for _ in range(SHARES_FOR_YOU):
    x = rand.getrandbits(16)
    y = polyeval(poly, x)
    shares.append((x, y))
print(shares)

secret = polyeval(poly, 0x48763)
key = sha256(str(secret).encode()).digest()[:16]
cipher = AES.new(key, AES.MODE_CTR)
print(cipher.encrypt(flag))
print(cipher.nonce)
