#!/usr/bin/env python3
from Crypto.Util.number import *
from random import getrandbits


flag = b'***********************REDACTED***********************'
FLAG = bytes_to_long(flag)

p = getStrongPrime(512)
q = getStrongPrime(512)
N = p * q
e = 17


menu = """ 
[1].CURR STATE
[2].ENCRYPT FLAG
[3].EXIT
"""

class PRNG(object):
    def __init__(self, seed1,seed2):
            self.seed1 = seed1
            self.seed2 = seed2
    
    @staticmethod
    def rotl(x, k):
            return ((x << k) & 0xffffffffffffffff) | (x >> 64 - k)
    
    def next(self):
            s0 = self.seed1
            s1 = self.seed2
            result = (s0 + s1) & 0xffffffffffffffff
            
            s1 ^= s0
            self.seed1 = self.rotl(s0, 55) ^ s1 ^ ((s1 << 14) & 0xffffffffffffffff)
            self.seed2 = self.rotl(s1, 36)
            
            return result

def main():
    a = getrandbits(64)
    b = getrandbits(64)
    g = PRNG(a,b)
     
    print("N : {}".format(N))
    print("e : {}".format(e))
    while True:
        print(menu)
        choice = input("$ ").rstrip().lstrip()
        
        if not choice in ["1","2","3"]:
            print("HIGH AF")
            exit()
            
        if choice == "1":
            print("state for you: {}".format(g.next()))
        
        elif choice == "2": 
            X = g.next()          
            ct = pow(FLAG + X, e, N) 
            print("ENC(flag+next_num): {}".format(ct))
        elif choice == "3":
            exit()
        
if __name__ ==  "__main__":
    main()
    
