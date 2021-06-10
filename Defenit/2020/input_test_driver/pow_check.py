#!/usr/bin/env python3

import os
import random
import hashlib

def getRand(length=4):
    table = '0123456789abcdef'
    return ''.join([random.choice(table) for i in range(length)])

def getPow():
    return hashlib.sha256(getRand().encode()).hexdigest()[-6:]

def checkPow(inp, out):
    if hashlib.sha256(inp.encode()).hexdigest()[-6:] == out:
        return True
    else:
        return False

def main():
    out = getPow()
    print('pow :', out)

    inp = input('solution : ')

    if checkPow(inp, out):
        os.system('./start.sh')
    else:
        print('sorry ^___^');

if __name__ == "__main__":
    main()
