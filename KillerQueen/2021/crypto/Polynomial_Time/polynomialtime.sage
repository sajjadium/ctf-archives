import time
import numpy as np
import random


def interpolate(l):
    for _ in range(624):
        x = random.getrandbits(32*2**4)
        print(x)
    mo = random.getrandbits(32*2**4)
    FR.<x> = PolynomialRing( IntegerModRing(mo) )
    f = prod([(random.getrandbits(32*2**4)*x-1) for _ in range(1,l)])
    return f, mo

#hmm, maybe a bit slow
def evaluate(poly, points, mo):
    evaluations = []
    
    for point in points:
        evaluations.append(poly(point))
    
    return evaluations

if __name__ == "__main__":
    with open("flag.txt","r") as f:
        flag = f.read()
    
    size = 1048576
    poly, mo = interpolate(size)
    R = Integers(mo)
    points = [R(random.getrandbits(32*2**4)) for _ in range(size)]
    ans = bytearray.fromhex(hex(prod(evaluate(poly,points,mo)))[2:-10])
    
    
    ciphertext = bytearray(b"")
    for i, c in enumerate(flag):
        ciphertext.append(ord(c)^^ans[i])
    
    print(ciphertext)