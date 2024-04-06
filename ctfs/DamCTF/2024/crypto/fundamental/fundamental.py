#!/usr/local/bin/python3

import secrets
import sys

p = 129887472129814551050345803501316649949


def poly_eval(coeffs, x):
    res = 0
    for c in coeffs:
        res = (c + x * res) % p
    return res


def pad(m):
    padlen = 16 - (len(m) % 16)
    padding = bytes([padlen] * padlen)
    return m + padding


def to_coeffs(m):
    coeffs = []
    for i in range(0, len(m), 16):
        chunk = m[i:i+16]
        coeffs.append(int.from_bytes(chunk))

    return coeffs


def auth(s, k, m):
    coeffs = to_coeffs(m)
    mac_int = (poly_eval(coeffs, k) + s) % p
    return mac_int.to_bytes(16)


def ver(s, k, m, t):
    return secrets.compare_digest(t, auth(s, k, m))


def hexinput(msg):
    try:
        return bytes.fromhex(input(msg))
    except ValueError:
        print("please enter a valid hex string")
        return None


k = secrets.randbelow(p)
kp = secrets.randbelow(p)
s = secrets.randbelow(p)
target = b"pleasepleasepleasepleasepleasepl"

print("Poly1305 is hard to understand so I decided to try simplifying it myself! Its parameters and stuff were probably just fluff right?")
print("Anyways it should be secure but if you can prove me wrong I'll give you a little something special :)")

print()
print("First I'll let you sign an arbitrary message")

while (msg1 := hexinput("message to sign (hex): ")) is None:
    pass

if len(msg1) == 0:
    print("message must be nonempty")
    sys.exit(1)
elif msg1 == target:
    print("nice try :)")
    sys.exit(1)

if len(msg1) % 16 != 0:
    mac = auth(s, kp, pad(msg1))
else:
    mac = auth(s, k, msg1)

print("authentication tag:", mac.hex())

print()
print("Now I just *might* give you the flag if you convince me my authenticator is insecure. Give me a valid tag and I'll give you the flag.")

while (tag := hexinput("enter verification tag (hex): ")) is None:
    pass

if ver(s, k, target, tag):
    print("oh you did it...here's your flag I guess")
    with open("flag") as f:
        print(f.read())

else:
    print("invalid authentication tag")
