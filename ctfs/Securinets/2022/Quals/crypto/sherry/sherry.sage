#!/usr/bin/env sage
from Crypto.Util.number import *
import random, sys, json

FLAG = "Securinets{REDACTED}"

def getRandomElement(F, deg):
        return F.random_element(degree=deg)

def polyToList(p):
        return p.list()

def listToPoly(F, l):
        return sum(F(c*x^i) for i, c in enumerate(l))

def polySum(p1, p2):
        if p1.parent() == p2.parent():
                return p1 + p2
        else:
                return p1 + p1.parent()(p2)

def getShare(g, secret):
        y = g^secret
        e = getRandomElement(PolynomialRing(GF(getPrime(256)), "x"), 10)
        s = polySum(y, e)
        share = polyToList(s)
        return share


if __name__ == '__main__':
        print(f"Welcome to Black Organization.\nTo join us, you have to guess our secret.\n")

        p = getStrongPrime(512)
        P = PolynomialRing(GF(p), "x")
        x = P.gen()
        N = getRandomElement(P, 10)
        Q.<x> = P.quotient_ring(N^2)

        G = Q(getRandomElement(P, 10))
        secret = random.randint(1, p-1)
        pub = G^secret

        params = {"N": polyToList(N), "pub": polyToList(pub), "G": polyToList(G), "p":p}
        print(f"{params}\n")

        for _ in range(5):
                try:
                        inp = json.loads(input("Your guess : "))
                        if 'g' not in inp or 's' not in inp:
                                raise ValueError("You must send a generator and a secret.")

                        g = listToPoly(Q, inp['g'])
                        s = int(inp['s'], 16) % p

                        if g^s == pub:
                                if s != secret:
                                        print(f"Don't cheat! :)")
                                        continue
                                print(f'From now, your name will be Sherry! Here is your flag : {FLAG}')
                                sys.exit()

                        else:
                                share = {'share': getShare(g, secret)}
                                print(f'{share}\n')

                except Exception as e:
                        print(e)
                        sys.exit()