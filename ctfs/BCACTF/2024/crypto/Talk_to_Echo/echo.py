from random import randint
from time import sleep
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
a = 0xffffffff00000001000000000000000000000000fffffffffffffffffffffffc
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
n = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
G = (0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296, 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5)

def add(p, q):
    if p == (0, 0):
        return q
    if q == (0, 0):
        return p
    if p[0] == q[0] and p[1] != q[1]:
        return (0, 0)
    if p != q:
        l = ((q[1] - p[1]) * pow(q[0] - p[0], -1, n)) % n
    else:
        if p[1] == 0:
            return (0, 0)
        l = ((3 * p[0] * p[0] + a) * pow(2 * p[1], -1, n)) % n
    x = (l * l - p[0] - q[0]) % n
    y = (l * (p[0] - x) - p[1]) % n
    return (x, y)

def mul(k, p):
    q = (0, 0)
    while k > 0:
        if k & 1:
            q = add(q, p)
        p = add(p, p)
        k >>= 1
    return q

priv = randint(1, n - 1)
pub = mul(priv, G)

def enc(m, key=0):
    if key == 0:
        r = randint(1, n - 1)
        R = mul(r, G)
        K = mul(r, pub)
    else:
        R = None
        K = key
    h = SHA256.new()
    h.update(str(K[0]).encode())
    k = h.digest()[:16]
    cipher = AES.new(k, AES.MODE_ECB)
    if R:
        return (R, cipher.encrypt(pad(m, 16)))
    return cipher.encrypt(pad(m, 16))

print("Hi! I'm Echo!")
print("Just a second, I just received a message... give me a bit as I read it...")
print(f"*mumbles* {enc(open("flag.txt", "rb").read())} *mumbles* ah interesting")
while True:
    print("Talk to me! Let's use Diffie-Hellman Key Exchange to stay secure.")
    print("Here is my public key:")
    print(pub)
    print("Please send me a point.")
    x = int(input("x: "))
    y = int(input("y: "))
    rA = (x, y)
    assert rA != (0, 0)
    K = mul(priv, rA)
    print(enc(b"Hey there! Thanks for talking to me :)", K))
    h = input("Want to speak again? (y/n)")
    if h.lower() != "y":
        break

