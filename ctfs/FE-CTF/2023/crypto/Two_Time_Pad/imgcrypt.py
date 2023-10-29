#!/usr/bin/env python3
import os
import sys
import itertools
from PIL import Image, ImageChops
from argon2.low_level import hash_secret_raw, Type

def expand_key(key, size):
    return hash_secret_raw(
        key,
        hash_len=size,
        salt=b'saltysalt',
        time_cost=1,
        memory_cost=1024,
        parallelism=1,
        type=Type.I,
    )

def imgcrypt(img, key):
    keyimg = Image.new(img.mode, img.size)
    keyimg.frombytes(expand_key(key, len(img.tobytes())))
    return ImageChops.add_modulo(img, keyimg)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f'usage: {sys.argv[0]} <keyfile> <inimg> <outimg>')
        exit(1)

    inimg = Image.open(sys.argv[2])

    keyfile = sys.argv[1]
    if os.path.exists(keyfile):
        with open(keyfile, 'rb') as f:
            key = f.read()
    else:
        print(f'Generating key; saving to {keyfile}')
        key = os.urandom(32)
        with open(keyfile, 'wb') as f:
            f.write(key)

    outimg = imgcrypt(inimg, key)
    outimg.save(sys.argv[3])
