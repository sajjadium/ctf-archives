#!/usr/bin/env python3
import os
import signal

from Cipher import BlockCipher

def handler(_signum, _frame):
    print("Time out!")
    exit(0)


def get_key():
    key = b''
    while len(key) < 9:
        b = os.urandom(1)
        if b[0] < 243:
            key += b
    return key


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(60)
    key = get_key()

    with open('flag', 'rb') as f:
        flag = f.read()
        flag += b'\x00' * ((-len(flag)) % 9)
    
    flag_cipher = BlockCipher(key, 20)
    enc_flag = b''
    for i in range(0, len(flag), 9):
        enc_flag += flag_cipher.encrypt(flag[i:i+9])
    print(f"enc_flag: {enc_flag.hex()}")

    cipher = BlockCipher(key, 4)
    while True:
        inp = bytes.fromhex(input("> "))
        assert len(inp) < (3 ** 7)
        assert all(b < 243 for b in inp)

        enc = b''
        for i in range(0, len(inp), 9):
            enc += cipher.encrypt(inp[i:i+9])
        
        print(f"Result: {enc.hex()}")


if __name__ == "__main__":
    main()
