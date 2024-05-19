from string import ascii_uppercase, digits
from itertools import permutations
from random import sample, seed, randint, choice
from os import urandom
from letter import letter

alphabet = ascii_uppercase + digits

seed(urandom(32))

keys_s = ["".join(sample(alphabet, len(alphabet))) for _ in range(3)]
key_x = "".join([choice(alphabet) for _ in range(5)])
keys_l = [randint(10, 20) for _ in range(4)]

def encrypt(text):
    text = text.upper()
    ct1 = ""

    i = 0
    ii = 0
    k1 = 0
    k2 = 0
    for c in text:
        if c in alphabet:
            if ii >= keys_l[k1]:
                ii = 0
                k1 = (k1 + 1) % len(keys_l)
                k2 = (k2 + 1) % len(keys_s)
            ct1 += keys_s[k2][alphabet.index(c)]
            i += 1
            ii += 1
        else:
            ct1 += c

    ct2 = ""
    i = 0
    for c in ct1:
        if c in alphabet:
            ix = (alphabet.index(c) + alphabet.index(key_x[i % len(key_x)])) % len(alphabet)
            ct2 += alphabet[ix]
            i += 1
        else:
            ct2 += c

    return ct2

print(encrypt(letter))

