from random import randrange
from Crypto.Util.number import inverse, long_to_bytes
from Crypto.Cipher import AES
from hashlib import sha256
import ast
import os
import signal

n = 256
p = 64141017538026690847507665744072764126523219720088055136531450296140542176327
a = 362
d = 1
q = 64141017538026690847507665744072764126693080268699847241685146737444135961328
c = 4
gx = 36618472676058339844598776789780822613436028043068802628412384818014817277300
gy = 9970247780441607122227596517855249476220082109552017755637818559816971965596

def xor(xs, ys):
    return bytes(x^y for x, y in zip(xs, ys))

def pad(b, l):
    return b + b"\0" + b"\xff" * (l - (len(b) + 1))

def unpad(b):
    l = -1
    while b[l] != 0:
        l -= 1
    return b[:l]

def add(P, Q):
    (x1, y1) = P
    (x2, y2) = Q

    x3 = (x1*y2 + y1*x2) * inverse(1 + d*x1*x2*y1*y2, p) % p
    y3 = (y1*y2 - a*x1*x2) * inverse(1 - d*x1*x2*y1*y2, p) % p
    return (x3, y3)

def mul(x, P):
    Q = (0, 1)
    x = x % q
    while x > 0:
        if x % 2 == 1:
            Q = add(Q, P)
        P = add(P, P)
        x = x >> 1
    return Q

def to_bytes(P):
    x, y = P
    return int(x).to_bytes(n // 8, "big") + int(y).to_bytes(n // 8, "big")

def send(msg, share):
    assert len(msg) <= len(share)
    print(xor(pad(msg, len(share)), share).hex())

def recv(share):
    inp = input()
    msg = bytes.fromhex(inp)
    assert len(msg) <= len(share)
    return unpad(xor(msg, share))

def main():
    signal.alarm(300)

    flag = os.environ.get("FLAG", "0nepoint{frog_pyokopyoko_3_pyokopyoko}")
    assert len(flag) < 2*8*n
    while len(flag) % 16 != 0:
        flag += "\0"

    G = (gx, gy)
    s = randrange(0, q)

    print("sG = {}".format(mul(s, G)))
    tG = ast.literal_eval(input("tG = "))  # you should input something like (x, y)
    assert len(tG) == 2
    assert type(tG[0]) == int and type(tG[1]) == int
    share = to_bytes(mul(s, tG))

    while True:
        msg = recv(share)
        if msg == b"flag":
            aes = AES.new(key=sha256(long_to_bytes(s)).digest(), mode=AES.MODE_ECB)
            send(aes.encrypt(flag.encode()), share)

        elif msg == b"quit":
            quit()

        else:
            send(msg, share)

if __name__ == '__main__':
    main()
