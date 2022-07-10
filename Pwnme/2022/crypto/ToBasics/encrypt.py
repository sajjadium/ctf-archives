#!/usr/bin/env python3
from secrets import choice
from string import digits

FLAG = open("./flag.txt", "r").read()
SECRET = choice(digits) * len(FLAG)

def encrypt(flag):
    return [str((ord(v[0]) ^ ord(v[1]))+i) for i, v in enumerate(zip(flag, SECRET))]


out = open('./flag-encrypted.txt', 'w')
out.write(','.join(encrypt(FLAG)))
