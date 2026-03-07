#!/usr/bin/env python3

import hashlib
import time
import random
from ecdsa import SigningKey, NIST256p

curve = NIST256p
n = curve.order

sk = SigningKey.generate(curve=curve)
vk = sk.verifying_key

secret_seed = random.getrandbits(16)

timestamp = int(time.time())

def bad_nonce(ts):
    data = str(ts).encode() + secret_seed.to_bytes(2, "big")
    k = hashlib.sha256(data).digest()
    return int.from_bytes(k, "big") % n

def sign_message(message: bytes):
    k = bad_nonce(timestamp)
    sig = sk.sign(message, k=k, hashfunc=hashlib.sha256, sigencode=lambda r, s, order: r.to_bytes(32, "big") + s.to_bytes(32, "big"))
    return sig.hex()


if __name__ == "__main__":

    messages = [
        b"Shokoladki eto moya zhizn.",
        b"Kyshaite shokoladki.",
        b"Bi-Bi prinesi shokoladok."
    ]

    print("Public key:")
    print(vk.to_string().hex())
    print()
    print("Timestamp used:", timestamp)
    print()

    for m in messages:
        print("Message:", m.decode())
        print("Signature:", sign_message(m))
        print()
