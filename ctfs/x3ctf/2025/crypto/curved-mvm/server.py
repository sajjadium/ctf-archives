from sage.all import *

import os
from json import dumps
from secrets import randbits
from Crypto.Util.number import bytes_to_long
from hashlib import sha1

FLAG = os.getenv("FLAG", "MVM{f4ke_fl4g}")

# a wonderful curve
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
Gx = 0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
Gy = 0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5

F = GF(p)
EC = EllipticCurve(F, [a, b])
n = EC.order()

SECRET_KEY = bytes_to_long(os.urandom(69420)) % n
G = EC([Gx, Gy])
assert G in EC

Q = SECRET_KEY * G

FUNNY_CREDITS_FOR_FREE_TRIAL = 2

CHALL_NAME = "Curved MVM"

K_SIZE = 18
SAMPLE_MSG = "hardcoded cuz reasons"
REQUIRED_MSG = "mvm mvm mvm"


def sign_msg(msg: str):
    z = bytes_to_long(sha1(msg.encode()).digest()) % n
    k = (randbits(K_SIZE) + 2) % n
    R = k * G
    r = ZZ(R.x()) % n
    s = (k.inverse_mod(n) * (z + r * SECRET_KEY)) % n
    return {"r": hex(r), "s": hex(s)}


def sign_bogus():
    return sign_msg(SAMPLE_MSG)


def verify_signature(r, s, msg):
    z = bytes_to_long(sha1(msg.encode()).digest()) % n

    if r < 1 or r >= n or s < 1 or s >= n:
        return {"error": "funny user uwu"}

    w = s.inverse_mod(n)

    u1 = (z * w) % n
    u2 = (r * w) % n

    P = u1 * G + u2 * Q

    should_r = ZZ(P.x()) % n

    if should_r == r:
        return {"flag": FLAG}
    else:
        # user funny
        return {"error": "invalid signature"}


def mvm():
    r = prompt_integer("r")
    s = prompt_integer("s")
    try:
        return verify_signature(r, s, REQUIRED_MSG)
    except:
        return {"error": "funny user"}


operations = {
    "sign": sign_bogus,
    "mvm": mvm,
}


def prompt_operation():
    _prompt = "/".join(operations)
    prompt = f"({_prompt}): "

    try:
        recv = input(prompt)
    except Exception:
        print("user too funny, complaints will be ignored\n")

    if recv not in operations:
        print("funny operation\n")
        return prompt_operation()

    return operations[recv]


def prompt_integer(name: str):
    prompt = f"{name}: "
    try:
        recv = input(prompt)
    except:
        print("user too funny, complaints will be sent to /dev/null\n")
        return prompt_integer(name)

    try:
        number = int(recv, 16)
    except:
        print("user supplied number too funny, complaints will be ignored\n")
        return prompt_integer(name)

    if number <= 1:
        print("user supplied number funny.\n")
        return prompt_integer(name)

    return ZZ(number)


funny_credits = FUNNY_CREDITS_FOR_FREE_TRIAL

if __name__ == "__main__":
    print(f"Welcome to {CHALL_NAME!r}, enjoy the pain!\n")

    while True:
        print(
            f"You have {funny_credits} funny credit{'s' if funny_credits > 1 else ''}."
        )
        operation = prompt_operation()
        print(dumps(operation()))
        funny_credits -= 1

        if funny_credits == 0:
            print("ran out of funny credits, bye")
            exit()

        print()
