#!/bin/python3
import os
import random
import des
import des.core
from Crypto.Util.number import *

from secret import FLAG

def shuffle(iterable):
    iterable = list(iterable)
    random.shuffle(iterable)
    return iterable

des.core.EXPANSION = shuffle(des.core.EXPANSION)
des.core.ROTATES = shuffle(des.core.ROTATES)
des.core.PERMUTATION = shuffle(des.core.PERMUTATION)
des.core.PERMUTED_CHOICE1 = shuffle(des.core.PERMUTED_CHOICE1)
des.core.PERMUTED_CHOICE2 = shuffle(des.core.PERMUTED_CHOICE2)
des.core.SUBSTITUTION_BOX = [shuffle(x) for x in des.core.SUBSTITUTION_BOX]

IV = os.urandom(8)

def encrypt(key, plaintext, IV):
    cipher = des.DesKey(key)
    return IV + cipher.encrypt(message = plaintext ,padding = True, initial=IV)

def encrypt_flag(key, IV):
    cipher = des.DesKey(key)
    return IV + cipher.encrypt(message = FLAG ,padding = True, initial=IV)

menu = '''E) encrypt
F) encrypt_flag
choice > '''

for _ in range(0x10000):
    choice = input(menu).upper()
    if choice == 'E':
        key = long_to_bytes(int(input('key(integer) > ')) | random.getrandbits(128), 16)
        plaintext = bytes.fromhex(input('plaintext(hex) > '))
        c = encrypt(key = key, plaintext = plaintext, IV = IV).hex()
    elif choice == 'F':
        key = long_to_bytes(int(input('key(integer) > ')) | random.getrandbits(128), 16)
        c = encrypt_flag(key = key, IV = IV).hex()
    else:
        quit()
    print('ciphertext > ' + c)

