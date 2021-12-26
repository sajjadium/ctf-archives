#! /usr/bin/python3 
from FLAG import flag
from Crypto.Util.number import *
import random
def genPrime():
    while True:
        a = random.getrandbits(512)
        b = random.getrandbits(512)

        if b % 3 == 0:
            continue

        p = a ** 2 + 3 * b ** 2
        if p.bit_length() == 1024 and p % 3 == 1 and isPrime(p):
            return p

def add(P, Q, mod):
    x1, y1 = P
    x2, y2 = Q

    if x2 is None:
        return P
    if x1 is None:
        return Q

    if y1 is None and y2 is None:
        x = x1 * x2 % mod
        y = (x1 + x2) % mod
        return (x, y)

    if y1 is None and y2 is not None:
        x1, y1, x2, y2 = x2, y2, x1, y1

    if y2 is None:
        if (y1 + x2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(y1 + x2, mod) % mod
            y = (x1 + y1 * x2) * inverse(y1 + x2, mod) % mod
            return (x, y)
        elif (x1 - y1 ** 2) % mod != 0:
            x = (x1 * x2 + 2) * inverse(x1 - y1 ** 2, mod) % mod
            return (x, None)
        else:
            return (None, None)
    else:
        if (x1 + x2 + y1 * y2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            y = (y1 * x2 + x1 * y2 + 2) * inverse(x1 + x2 + y1 * y2, mod) % mod
            return (x, y)
        elif (y1 * x2 + x1 * y2 + 2) % mod != 0:
            x = (x1 * x2 + (y1 + y2) * 2) * inverse(y1 * x2 + x1 * y2 + 2, mod) % mod
            return (x, None)
        else:
            return (None, None)

def myPower(P, a, mod):
    target = (None, None)
    t = P
    while a > 0:
        if a % 2:
            target = add(target, t, mod)
        t = add(t, t, mod)
        a >>= 1
    return target

def gennewkeys():
    N = p*q
    d = getPrime(350)
    e = inverse(d, PHI)
    return e,N

p, q = genPrime(),genPrime()


PHI = (p-1)*(q-1)
N = p*q
d = getPrime(350)

e = inverse(d, PHI)

banner = """
[1] get my pubkey
[2] gen a new key
[3] give me flag
[4] exit
"""

while 1:
    print(banner)
    op = input(">")
    if(op=='1'):
        print("here you are")
        print(f'e:{e} N:{N}')
    if(op=='2'):
        print(r"oh you don't like my key:(")
        e,N = gennewkeys()
        print(f'e:{e} N:{N}')
    if(op=="3"):
        print('wait for secs...')
        
        
        ln = len(flag)
        pt1, pt2 = flag[: ln // 2], flag[ln // 2 :]
        M = (bytes_to_long(pt1), bytes_to_long(pt2))
        pad = genPrime()
        
        finitN = N*pad
        cipher = myPower(M, e, finitN)
        print(f"cipher:{cipher}")
        print(f"padding:{pad}")
        print(r"c you next time")
        exit()
    if(op=='4'):
        exit()
    
    
