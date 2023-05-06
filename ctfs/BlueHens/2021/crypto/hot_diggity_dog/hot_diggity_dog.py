from Crypto.Util.number import *
from os import urandom

def getKey():
    e = 3
    t = 3
    while not GCD(e,t) == 1:
        p = getStrongPrime(1024)
        q = getStrongPrime(1024)
        N = p*q
        t = (p-1)*(q-1)
        e = bytes_to_long(urandom(256))
    return N,e

def encrypt(pt,N,e):
    try:
        pt = bytes(pt,'utf-8')
    except:
        pass

    assert bytes(pt) == pt,"ERROR: plaintext must be string or byte string!"
    pt = bytes_to_long(pt)

    return pow(pt,e,N)



N,e = getKey()

f = open("flag.txt")
pt = f.read()
f.close()

f = open("output.txt",'w')

ct = encrypt(pt,N,e)

output = "ct="+ str(ct) + "\n\ne="+str(e) + "\n\nN=" + str(N)

f.write(output)
f.close()