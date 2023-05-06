#!/usr/bin/env python3.8
from Crypto.Util.number import inverse
from Crypto.Cipher import AES
from collections import namedtuple
import random, sys, os, signal, hashlib

FLAG = "FwordCTF{#######################################################}"

WELCOME = '''
Welcome to my Invincible Game, let's play.
If you can decrypt all my messages that I will give, You win.
                (( _______
     _______      /\O    O\ 
    /O     /\    /  \      \ 
   /   O  /O \  / O  \O____O\ ))
((/_____O/    \ \    /O     /
  \O    O\    /  \  /   O  /
   \O    O\ O/    \/_____O/
    \O____O\/ ))

You get to choose your point first.
'''

Point = namedtuple("Point","x y")

class EllipticCurve:
    INF = Point(0, 0)

    def __init__(self, a, b, Gx, Gy, p):
        self.a = a
        self.b = b
        self.p = p
        self.G = Point(Gx, Gy)

    def add(self, P, Q):
        if P == self.INF:
            return Q
        elif Q == self.INF:
            return P

        if P.x == Q.x and P.y == (-Q.y % self.p):
            return self.INF
        if P != Q:
            tmp = (Q.y - P.y)*inverse(Q.x - P.x, self.p) % self.p
        else:
            tmp = (3*P.x**2 + self.a)*inverse(2*P.y, self.p) % self.p
        Rx = (tmp**2 - P.x - Q.x) % self.p
        Ry = (tmp * (P.x - Rx) - P.y) % self.p
        return Point(Rx, Ry)
        
    def multiply(self, P, n):
        R = self.INF
        while 0 < n:
            if n & 1 == 1:
                R = self.add(R, P)
            n, P = n >> 1, self.add(P, P)
        return R

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
a = -0x3
Gx = 0x55b40a88dcabe88a40d62311c6b300e0ad4422e84de36f504b325b90c295ec1a
Gy = 0xf8efced5f6e6db8b59106fecc3d16ab5011c2f42b4f8100c77073d47a87299d8
b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
E = EllipticCurve(a, b, Gx, Gy, p)

class RNG:
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def next(self):
        s = E.multiply(self.P, self.seed).x
        self.seed = s
        r = E.multiply(self.Q, s).x
        return r & ((1<<128) - 1)

def encrypt(msg, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipher = aes.encrypt(msg)
    return iv + cipher

def decrypt(cipher, key, iv):
    aes = AES.new(key, AES.MODE_CBC, iv)
    msg = aes.decrypt(cipher)
    return msg


class Invincible:
    def __init__(self):
        print(WELCOME)

    def start(self):
        try:
            Px = int(input("Point x : "))
            Py = int(input("Point y : "))
            P = Point(Px, Py)
            if (P == E.INF) or (Px == 0) or (Py == 0):
                print("Don't cheat.")
                sys.exit()
            print(f"Your point : ({P.x}, {P.y})")

            Q = E.multiply(E.G, random.randrange(1, p-1))
            print(f"\nMy point : ({Q.x}, {Q.y})")

            rng = RNG(random.getrandbits(128), P, Q)

            for _ in range(100):
                key = hashlib.sha1(str(rng.next()).encode()).digest()[:16]
                iv = os.urandom(16)
                msg = os.urandom(64)
                cipher = encrypt(msg, key, iv) 
                print(f"\nCiphertext : {cipher.hex()}")
                your_dec = bytes.fromhex(input("What was the message ? : "))
                if your_dec == msg:
                    print("Correct.")
                else:
                    print("You lost.")
                    sys.exit()

            print(f"Congratulations ! Here's your flag : {FLAG}")

        except Exception:
            print("System error.")
            sys.exit()


signal.alarm(360)
if __name__ == "__main__":
    challenge = Invincible()
    challenge.start()