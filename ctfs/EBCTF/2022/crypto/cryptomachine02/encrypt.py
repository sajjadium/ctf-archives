#!/usr/bin/python

import sys, binascii, base64, string, random

if len(sys.argv) < 2:
    print "Usage: %s <flag>" % sys.argv[0]
    sys.exit(1)

flag = sys.argv[1]

def H(m):
    return binascii.hexlify(m)

def B(m):
    return base64.b64encode(m)

def R(m):
    t = string.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz:",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm#")
    return string.translate(m,t)

def X(m):
    return H(''.join(chr(ord(c)^0x42) for c in m))

def encrypt(s):
    out = s
    f = [ X, B, R ]
    for i in range(random.randint(8,14)):
        a = random.randint(1,len(out)/2)
        b = random.randint(a+1,len(out)-1)
	tmp = [out[0:a],out[a:b],out[b:]]
	for j in range(3):
	    k = random.randint(0,2)
	    tmp[j] = str(k) + f[k](tmp[j])
	out = ':'.join(tmp)
    return out
        

if __name__ == "__main__":
    open("MESSAGE", "wb").write(encrypt(flag))
