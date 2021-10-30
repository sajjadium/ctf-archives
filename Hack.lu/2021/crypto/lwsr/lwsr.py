#!/usr/bin/env sage
from os import urandom
from sage.crypto.lwe import Regev
import sys

flag = b"flag{this_may_look_like_a_real_flag_but_its_not}"

def lfsr(state):
    # x^384 + x^8 + x^7 + x^6 + x^4 + x^3 + x^2 + x + 1
    mask   = (1 << 384) - (1 << 377) + 1
    newbit = bin(state & mask).count('1') & 1
    return (state >> 1) | (newbit << 383)


# LFSR initalization
state = int.from_bytes(urandom(384 // 8), "little")
assert state != 0

# Regev KeyGen
n = 128
m = 384

lwe = Regev(n)
q   = lwe.K.order()
pk  = [list(lwe()) for _ in range(m)]
sk  = lwe._LWE__s

# publish public key
print(f"Public key (q = {q}):")
print(pk)

# encrypt flag
print("Encrypting flag:")
for byte in flag:
    for bit in map(int, format(byte, '#010b')[2:]):
        # encode message
        msg = (q >> 1) * bit
        assert msg == 0 or msg == (q >> 1)

        # encrypt
        c = [vector([0 for _ in range(n)]), 0]
        for i in range(m):
            if (state >> i) & 1 == 1:
                c[0] += vector(pk[i][0])
                c[1] += pk[i][1]

        # fix ciphertext
        c[1] += msg
        print(c)

        # advance LFSR
        state = lfsr(state)


# clear LFSR bits
for _ in range(384):
    state = lfsr(state)

while True:
    # now it's your turn :)
    print("Your message bit: ")
    msg = int(sys.stdin.readline())
    if msg == -1:
        break
    assert msg == 0 or msg == 1

    # encode message
    pk[0][1] += (q >> 1) * msg

    # encrypt
    c = [vector([0 for _ in range(n)]), 0]
    for i in range(m):
        if (state >> i) & 1 == 1:
            c[0] += vector(pk[i][0])
            c[1] += pk[i][1]

    # fix public key
    pk[0][1] -= (q >> 1) * msg

    # check correctness by decrypting
    decrypt = ZZ(c[0].dot_product(sk) - c[1])
    if decrypt >= (q >> 1):
        decrypt -= q
    decode = 0 if abs(decrypt) < (q >> 2) else 1
    if decode == msg:
        print("Success!")
    else:
        print("Oh no :(")

    # advance LFSR
    state = lfsr(state)
