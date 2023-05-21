import os
import sys
from flag import FLAG


def xor(key, data):
    return bytes(ac ^ bc for ac, bc in zip(key*len(data), data))


def viscrypt(data):
    return xor(data, data[1:] + b"\xaa")


def round(key, rawdata):
    return viscrypt(xor(key, rawdata))


key = os.urandom(8)

pt = FLAG
for i in range(8833):
    pt = round(key, pt)

print(pt.hex())
