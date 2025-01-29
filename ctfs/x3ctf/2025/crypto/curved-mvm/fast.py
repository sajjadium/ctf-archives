import os
from json import dumps
from secrets import randbits
from hashlib import sha1
from fastecdsa.curve import P256
from fastecdsa.point import Point

n = P256.q

FLAG = os.getenv("FLAG", "MVM{f4ke_fl4g}")

SECRET_KEY = int.from_bytes(os.urandom(69420)) % n

Q = SECRET_KEY * P256.G

FUNNY_CREDITS_FOR_FREE_TRIAL = 2

CHALL_NAME = "Curved MVM"

K_SIZE = 18
SAMPLE_MSG = "hardcoded cuz reasons"
REQUIRED_MSG = "mvm mvm mvm"


def sign_msg(msg: str):
    z = int.from_bytes(sha1(msg.encode()).digest()) % n
    k = (randbits(K_SIZE) + 2) % n
    R = k * P256.G
    r = R.x % n
    s = (pow(k, -1, n) * (z + r * SECRET_KEY)) % n
    return {"r": hex(r), "s": hex(s)}


def sign_bogus():
    return sign_msg(SAMPLE_MSG)


def verify_signature(r, s, msg):
    z = int.from_bytes(sha1(msg.encode()).digest()) % n

    if r < 1 or r >= n or s < 1 or s >= n:
        return {"error": "funny user uwu"}

    w = pow(s, -1, n)

    u1 = (z * w) % n
    u2 = (r * w) % n

    P = u1 * P256.G + u2 * Q

    should_r = P.x % n

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

    return number


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
