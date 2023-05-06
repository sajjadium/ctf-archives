#!/usr/bin/env python3
import math
import binascii
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long, long_to_bytes

def chunks(l, n):
    assert(len(l) % n == 0)
    for i in range(0, len(l), n):
        yield l[i:i+n]

FLAG_LEN = 72
M_SIZE = math.isqrt(FLAG_LEN * 8)

flag = input("What is your key? ")
assert(len(flag) == FLAG_LEN)
# turn flag into a matrix
inter_key = bin(int(flag.encode('ascii').hex(), 16))[2:].rjust(FLAG_LEN * 8, '0')
key = [[int(c) for c in l] for l in chunks(inter_key, M_SIZE)]


def encrypt(ptxt):
    assert len(ptxt) == M_SIZE
    enc = [0] * M_SIZE
    for i in range(M_SIZE):
        for j in range(M_SIZE):
            if key[i][j] == 1:
                enc[i] ^= ptxt[j]
    return binascii.hexlify(bytes(enc))

def decrypt(ctxt):
    return "todo"

while True:
    print("Would you like to encrypt (E), decrypt (D), or quit (Q)?", flush=True)
    l = input(">>> ").strip().upper()
    if (len(l) > 1):
        print("You inputted more than one character...", flush=True)
    elif (l == "Q"):
        print("Thank you for using the Gray-Scott model of encryption!", flush=True)
        exit()
    elif (l == "E"):
        print("What would you like to encrypt?", flush=True)
        I = input(">>> ").strip().encode('ascii')
        c = b''.join([encrypt(i) for i in chunks(pad(I, M_SIZE), M_SIZE)])
        print("Your encrypted message is:", c.decode('ascii'), flush=True)
    elif (l == "D"):
        print("What was the message?", flush=True)
        I = input(">>> ").strip()
        m = b''.join([decrypt(i) for i in chunks(I, 2 * M_SIZE)])
        print("Your decrypted message is:", unpad(m, M_SIZE), flush=True)
        