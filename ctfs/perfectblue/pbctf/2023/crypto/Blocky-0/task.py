#!/usr/bin/env python3
import hashlib
import os
import signal

from Cipher import BlockCipher
from GF import GF

def handler(_signum, _frame):
    print("Time out!")
    exit(0)


def get_random_block():
    block = b''
    while len(block) < 9:
        b = os.urandom(1)
        if b[0] < 243:
            block += b
    return block


def get_mac(pt):
    mac = hashlib.sha256(pt).digest()[:9]
    return bytes([x % 243 for x in mac])


def pad(pt):
    mac = get_mac(pt)
    v = 9 - len(pt) % 9
    return pt + bytes([v] * v) + mac


def unpad(pt):
    if len(pt) < 18 or len(pt) % 9 != 0:
        return
    pt, mac = pt[:-9], pt[-9:]
    if not (1 <= pt[-1] <= 9):
        return
    
    pt = pt[:-pt[-1]]
    if mac == get_mac(pt):
        return pt


def add(a, b):
    return bytes([(GF(x) + GF(y)).to_int() for x, y in zip(a, b)])


def sub(a, b):
    return bytes([(GF(x) - GF(y)).to_int() for x, y in zip(a, b)])


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60)
    key = get_random_block()
    cipher = BlockCipher(key, 20)

    while True:
        inp = input("> ")

        if inp == 'E':
            inp = input("Input (in hex): ")
            inp = bytes.fromhex(inp)
            assert len(inp) < 90
            assert all(b < 243 for b in inp)

            if inp == 'gimmeflag':
                print("Result: None")
                continue

            pt = pad(inp)
            iv = get_random_block()
            enc = iv

            for i in range(0, len(pt), 9):
                t = add(pt[i:i+9], iv)
                iv = cipher.encrypt(t)
                enc += iv
            
            print(f"Result: {enc.hex()}")
        elif inp == 'D':
            inp = input("Input (in hex): ")
            inp = bytes.fromhex(inp)
            assert len(inp) < 108
            assert all(b < 243 for b in inp)

            iv, ct = inp[:9], inp[9:]
            dec = b''

            for i in range(0, len(ct), 9):
                t = cipher.decrypt(ct[i:i+9])
                dec += sub(t, iv)
                iv = ct[i:i+9]

            pt = unpad(dec)
            if pt == b'gimmeflag':
                with open('flag', 'r') as f:
                    flag = f.read()
                    print(flag)
                exit(0)
            elif pt:
                print(f"Result: {pt.hex()}")
            else:
                print("Result: None")


if __name__ == "__main__":
    main()
