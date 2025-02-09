#!/usr/local/bin/python3
from VDF import verify_proof
from Crypto.Util.number import getPrime, isPrime
import os
from math import gcd
def is_valid(p, n):
    assert gcd(p,n) == 1
    return 1 < p < n - 1
if __name__ == "__main__":
    print("Show me that you're a man of patience and I will give you the flag")
    p = getPrime(20)
    q = getPrime(20)
    N = p * q
    g = getPrime(40)
    print("g = ", g)
    y = int(input("y: ")) % N
    if not is_valid(y, N):
        print("Must be in the group")
        exit()
    print("N = ", N) # Forgot to give you this
    logT = int(input("logT: "))
    if logT.bit_length() > 10:
        print("Your proof is too long")
        exit()
    pi = []
    for i in range(logT):
        t = int(input("pi: "))
        if not is_valid(t, N):
            print("Must be in the group")
            exit()
        pi.append(t % N) 
    
    print("Verifying")
    ok = verify_proof(g, y, pi, logT, 0, N)
    if ok and logT > 64:
        with open("flag.txt", "r") as f:
            flag = f.read()
            print(flag)
    else:
        print("Good things come to those who wait")
        exit()

