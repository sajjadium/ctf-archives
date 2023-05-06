from secret import flag
from Crypto.Util.number import bytes_to_long, getStrongPrime, inverse
from hashlib import sha256
import os

def prepare(m):
    if len(m)>64:
        m = m[:64]
    elif len(m)<64:
        l = 64-len(m)
        m = m + os.urandom(l)
    assert len(m) == 64
    return (m[:32],m[32:])

def sign(m,n,d):
    sign = pow(bytes_to_long(sha256(m[1]).digest())^bytes_to_long(m[0]), d, n)
    return hex(sign)[2:]

#doesn't even work, lol
def verify(m,s,n,e):
    return pow(int(s,16),e,n) == bytes_to_long(sha256(m[1]).digest())^bytes_to_long(m[0])

p,q = getStrongPrime(1024), getStrongPrime(1024)
n = p*q
e = 65537
d = inverse(e, (p-1)*(q-1))

while True:
    print()
    print("1. Sign")
    print("2. Sign but better")
    print("3. Verify")
    print("4. See key")
    print("0. Exit")
    c = int(input("> "))
    if c == 0:
        break
    elif c == 1:
        msg = input("> ").encode()
        print(sign(prepare(msg),n,d))
    elif c == 2:
        msg = input("> ").encode()
        print(sign(prepare(flag+msg),n,d))
    elif c == 3:
        msg = input("> ").encode()
        s = input("> ")
        print(verify(prepare(msg),s,n,e))
    elif c == 4:
        print("N:",n)
        print("e:",e)
    else:
        print("plz don't hack")
        break
