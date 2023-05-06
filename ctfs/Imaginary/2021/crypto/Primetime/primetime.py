#!/usr/bin/env python3

from itertools import islice
from math import gcd
from random import randint

ELEMENT_LEN = 16

def primes():
    num = 2
    while True:
        prime = 1
        for i in range(2, num):
            if num%i == 0:
                prime = 0
        if prime:
            yield num
        num += 1


class Element:
    def __init__(self, n):
        self.n = Element.reduce(n)

    def __str__(self):
        return str(self.n)

    def __add__(self, other):
        return Element(self.n*other.n)

    def __eq__(self, other):
        return self.n == other.n

    def __mul__(self, n):
        if type(n) == int:
            ret = Element(1)
            for c in "{:0128b}".format(n):
                ret += ret
                if c == '1':
                    ret += self
            return ret
        if type(n) == Element:
            ret = Element(1)
            primelist = list(islice(primes(), ELEMENT_LEN))
            for i, num in enumerate(primelist[::-1]):
                cnt = 0
                temp = n.n
                while gcd(temp, num) > 1:
                    cnt += 1
                    temp //= num
                for c in "{:08b}".format(cnt):
                    ret += ret
                    if c == '1':
                        ret += self
            return ret

    @staticmethod
    def encode(b):
        assert len(b) <= ELEMENT_LEN
        ret = 1
        for i, num in enumerate(primes()):
            if i >= len(b):
                return Element(ret)
            ret *= num**b[i]

    @staticmethod
    def reduce(n):
        if n == 0:
            return 0
        primelist = list(islice(primes(), ELEMENT_LEN))
        for i, num in enumerate(primelist):
            while n % (num**256) == 0:
                n //= num**256
                if num != primelist[-1]:
                    n *= primelist[i+1]
        return n


if __name__ == '__main__':
    gen = Element.encode(b"+h3_g3n3ra+0r_pt")
    akey = randint(1, 2**128)|1
    bkey = randint(1, 2**128)|1

    apub = gen*akey
    bpub = gen*bkey

    s = gen*akey*bkey

    flag = open("flag.txt").read()
    flag = flag.replace("ictf{", "").replace("}", "").encode()
    assert len(flag) == ELEMENT_LEN

    m = Element.encode(flag)
    ct = m*s

    print("gen =", gen)
    print("apub =", apub)
    print("bpub =", bpub)
    print("ct =", ct)
