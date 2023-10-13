#!/usr/bin/env python3

import secrets
import os, sys, hmac
import cryptod
from proofofwork import challenge_proof_of_work

FLAG = os.environ.get("FLAG", "flag{FAKE_FLAG}") if "flag" in os.environ.get("FLAG","") else "flag{FAKE_FLAG}"


 
def main():
    print("Welcome to the Spooky Safebox!")
    if not challenge_proof_of_work():
        return
    kpriv, kpub = cryptod.make_keys()
    order = cryptod.get_order()
    encrypted_flag = cryptod.encrypt(kpub, FLAG)
    print("Here is the encrypted flag:", encrypted_flag)
    print("You've got 9 signatures, try to recover Satoshi's private key!")
    for i in range(9):
        msg_ = input("Enter a message to sign: >")
        msg = hmac.new(cryptod.int_to_bytes(kpub.point.x() * i), msg_.encode(), "sha224").hexdigest()
        checksum = 2**224 + (int(hmac.new(cryptod.int_to_bytes(kpriv.secret_multiplier) , msg_.encode(), "sha224").hexdigest(), 16) % (order-2**224))
        nonce = secrets.randbelow(2 ** 224 - 1) + 1 + checksum
        sig = kpriv.sign(int(msg, 16) % order, nonce)
        print("Signature",(cryptod.int_to_bytes(int(sig.r)) + bytes.fromhex("deadbeef") + cryptod.int_to_bytes(int(sig.s))).hex())
    
    print("Goodbye!")

if __name__ == '__main__':
    try:
        main()
    except EOFError:
        pass
    except KeyboardInterrupt:
        pass
