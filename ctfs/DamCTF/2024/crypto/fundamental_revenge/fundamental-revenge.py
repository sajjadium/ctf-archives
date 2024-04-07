#!/usr/local/bin/python3

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
import sys

p = 168344944319507532329116333970287616503


def F(k, x):
    f = Cipher(algorithms.AES(k), modes.ECB()).encryptor()
    return f.update(x) + f.finalize()


def poly_eval(coeffs, x):
    res = 0
    for c in coeffs:
        res = (c + x * res) % p
    return res


def to_coeffs(m):
    coeffs = [1]
    for i in range(0, len(m), 16):
        chunk = m[i : i + 16]
        coeffs.append(int.from_bytes(chunk))

    return coeffs


def auth(k, s, m):
    coeffs = to_coeffs(m)
    poly_k = int.from_bytes(k[16:])
    mac_int = (poly_eval(coeffs, poly_k) + s) % p
    return F(k[:16], mac_int.to_bytes(16))


def ver(k, s, m, t):
    return secrets.compare_digest(auth(k, s, m), t)


def hexinput(msg):
    try:
        b = bytes.fromhex(input(msg))
        assert len(b) % 16 == 0 and len(b) > 0
        return b
    except (ValueError, AssertionError):
        print("please enter a valid hex string")
        return None


k = secrets.token_bytes(32)
s = secrets.randbelow(p)

target = b"gonna ace my crypto final with all this studying"

print("Let's try this again, shall we?")
print()

while (msg1 := hexinput("first message to sign (hex): ")) is None:
    pass

if msg1 == target:
    print("nice try :)")
    sys.exit(1)

mac = auth(k, s, msg1)
print("authentication tag:", mac.hex())

print()
print("now sign this:", target.decode())

while (tag := hexinput("enter verification tag (hex): ")) is None:
    pass

if ver(k, s, target, tag):
    print("oh you did it again...I guess I'm just bad at cryptography :((")
    with open("flag") as f:
        print("here's your flag again..", f.read())

else:
    print("invalid authentication tag")
