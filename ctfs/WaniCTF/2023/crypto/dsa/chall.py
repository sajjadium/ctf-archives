from Crypto.Util.number import isPrime
from hashlib import sha256
from os import getenv
from random import randbytes
import re

q = 139595134938137125662213161156181357366667733392586047467709957620975239424132898952897224429799258317678109670496340581564934129688935033567814222358970953132902736791312678038626149091324686081666262178316573026988062772862825383991902447196467669508878604109723523126621328465807542441829202048500549865003
p = 2 * q + 1
g = 2
assert isPrime(p)
assert isPrime(q)

FLAG = getenv("FLAG", "FAKE{NOTE:THIS_IS_NOT_THE_FLAG}")
assert len(FLAG) < 32


def keygen(p: int, q: int, g: int):
    x = int(randbytes(48).hex(), 16)
    y = pow(g, x, p)
    return x, y


def sign(message: str, x: int):
    k = pow(int.from_bytes(message.encode(), "big"), -1, q)
    r = pow(g, k, p) % q
    h = sha256(message.encode()).hexdigest()
    s = pow(k, -1, q) * (int(h, 16) + x * r) % q
    return h, r, s


def verify(message_hash: str, r: int, s: int, y: int):
    message_hash = int(message_hash, 16)
    w = pow(s, -1, q)
    u1 = message_hash * w % q
    u2 = r * w % q
    v = (pow(g, u1, p) * pow(y, u2, p) % p) % q
    return v == r


x, y = keygen(p, q, g)
print(f"p = {p}")
print(f"q = {q}")
print(f"g = {g}")
print(f"y = {y}")
hash, r, s = sign(FLAG, x)
assert verify(hash, r, s, y)
print("FLAG = {}".format(re.sub(r"([\S+])", r"*", FLAG)))
print(f"sha256(FLAG) = {hash}")
print(f"r = {r}")
print(f"s = {s}")
