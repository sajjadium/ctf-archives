# /usr/bin/env python
import sys
from Crypto.Util.number import (
    getPrime,
    getRandomInteger,
    isPrime,
    bytes_to_long,
    long_to_bytes,
)
from hashlib import sha256
from flag import flag

nbits = 1024
# openssl prime -generate -bits 1024 -safe
p = 157177458027947738464608587718505170872557537311336022386936190418737852141444802600222526305430833558655717806361264485789209743716195302937247478034883845835496282499162731072456548430299962306072692670825782721923481661135742935447793446928303177027490662275563294516442565718398572361235897805000082380599

# Nobody wants dlog to be so easy
assert isPrime(p)
assert isPrime((p - 1) // 2)
assert p.bit_length() == 1024

q = getPrime(100)
print(f"{q=}")

s = getRandomInteger(nbits)
g = 25
gs = pow(g, s, p)
print(f"{gs=}")


def weird_schnorr_sign(m, x):
    k = getRandomInteger(nbits)
    r = pow(g, k, p)
    e = bytes_to_long(sha256(long_to_bytes(r) + long_to_bytes(m)).digest())
    s = (k + x * e) % ((p - 1) // 2)
    return [s, e]


def weird_schnorr_verify(m, s, e, y):
    r = pow(g, s, p) * pow(y, -e, p) % p
    ep = bytes_to_long(sha256(long_to_bytes(r) + long_to_bytes(m)).digest())
    return e == ep

def nxt(m):
    return bytes_to_long(sha256(long_to_bytes(m)).digest())

def sign(m, s):
    ta = [getRandomInteger(100)] * 4
    cc = [nxt(m % q)]
    for i in range(3):
        cc += [nxt(cc[-1])]
    sta = (m - sum([pow(g, b, p) * c % p for b, c in zip(ta, cc)])) % q
    r = getRandomInteger(100)
    a = (p - 1 - s) * p - (q * r + sta) * (p - 1)
    assert a * gs * pow(g, a, p) % p == q * r + sta
    return weird_schnorr_sign(a, s) + [a] + ta


def verify(m, sig, gs):
    s, e, st = sig[0], sig[1], sig[2:]
    if len(st) < 5:
        return False
    if not weird_schnorr_verify(st[0], s, e, gs):
        return False
    cc = [nxt(m % q)]
    for i in range(len(st) - 2):
        cc += [nxt(cc[-1])]
    mp = st[0] * gs * pow(g, st[0], p) % p + sum([
        pow(g, x, p) * c % p for x, c in zip(st[1:], cc)
    ])
    return mp % q == m % q


msg = b"this is just a test so that you trust the algo"
sm = sign(bytes_to_long(msg), s)
assert verify(bytes_to_long(msg), sm, gs)
print(f"{sm=}")

leak = bytes_to_long(flag) % q
print(f"{leak=}")

print("Give me valid signature for flag:")
MAX_LINE = 2 ** 14
line = sys.stdin.readline(MAX_LINE + 1)
if len(line) > MAX_LINE:
    print("Do you want to break the server of what?")
else:
    sig = list(map(int, line.split(",")))
    if verify(bytes_to_long(flag), sig, gs):
        print(flag.decode())
    else:
        print(
            "Verification failed!\nHopefully next time you succeed, keep going!"
        )
