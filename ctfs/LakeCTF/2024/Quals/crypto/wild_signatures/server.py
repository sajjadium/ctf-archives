#!/usr/bin/env python3
import os

from Crypto.PublicKey import ECC
from Crypto.Signature import eddsa

flag = os.environ.get("FLAG", "EPFL{test_flag}")

msgs = [
    b"I, gallileo, command you to give me the flag",
    b"Really, give me the flag",
    b"can I haz flagg",
    b"flag plz"
]

leos_key = ECC.generate(curve='ed25519')
sigs = [ leos_key.public_key().export_key(format='raw') + eddsa.new(leos_key, 'rfc8032').sign(msg) for msg in msgs]

def parse_and_vfy_sig(sig: bytes, msg: bytes):
    pk_bytes = sig[:32]
    sig_bytes = sig[32:]
    
    pk = eddsa.import_public_key(encoded=pk_bytes)

    if pk.pointQ.x == 0:
        print("you think you are funny")
        raise ValueError("funny user")

    eddsa.new(pk, 'rfc8032').verify(msg, sig_bytes)

if __name__ == "__main__":
    try:
        print("if you really are leo, give me public keys that can verify these signatures")
        for msg, sig in zip(msgs, sigs):
            print(sig[64:].hex())
            user_msg = bytes.fromhex(input())

            # first 64 bytes encode the public key
            if len(user_msg) > 64 or len(user_msg) == 0:
                print("you're talking too much, or too little")
                exit()

            to_verif = user_msg + sig[len(user_msg):]

            parse_and_vfy_sig(to_verif, msg)
            print("it's valid")

    except ValueError as e:
        print(e)
        exit()

    print(flag)
