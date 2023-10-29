#!/usr/bin/env python3
from Crypto.Util.number import (
    bytes_to_long, long_to_bytes
)
from hashlib import md5
import os, signal
import sys
import random

BITS = 128

class ClawCrane(object):
    def __init__(self) -> None:
        self.seed = bytes_to_long(os.urandom(BITS//8))
        self.bless = 0
        self.score = 0
    
    def get_input(self, prompt="> "):
        print(prompt, end="")
        sys.stdout.flush()
        return input()
    
    def check_pos(self, pos, moves):
        col, row = 0, 0
        for move in moves:
            if move == "W":
                if row < 15: row += 1
            elif move == "S":
                if row > 0: row -= 1
            elif move == "A":
                if col > 0: col -= 1
            elif move == "D":
                if col < 15: col += 1
            else:
                return -1
        print(col, row)
        return pos == [col, row]
    
    def gen_chaos(self, inp):
        def mapping(x):
            if x=='W': return "0"
            if x=='S': return "1"
            if x=='A': return "2"
            if x=='D': return "3"
        vs = int("".join(map(mapping, inp)), 4)
        chaos = bytes_to_long(md5(
                    long_to_bytes((self.seed + vs) % pow(2,BITS))
                ).digest())
        self.seed = (self.seed + chaos + 1) % pow(2,BITS)
        return chaos
    
    def destiny_claw(self, delta):
        bits = bin(delta)[2:]
        if len(bits) < 128+self.bless:
            bits += "0"*(128+self.bless - len(bits))
        c = random.choice(bits)
        if c=='0': return True
        else: return False
    
    def run(self):
        pos = [random.randrange(1,16), random.randrange(1,16)]
        moves = self.get_input(f"i am at {pos}, claw me.\nYour moves: ")
        if len(moves) > 100:
            print("too many steps")
            return
        if not self.check_pos(pos, moves):
            print("sorry, clawed nothing")
            return
        r = self.gen_chaos(moves[:64])
        print(f"choas: {r}")
        p, q = map(int, self.get_input(f"give me your claw using p,q and p,q in [0, 18446744073709551615] (e.g.: 1,1): ").split(","))
        if not (p>0 and p<pow(2,BITS//2) and q>0 and q<pow(2,BITS//2)):
            print("not in range")
            return
        delta = abs(r*q - p*pow(2,BITS))
        if self.destiny_claw(delta):
            self.score += 10
            self.bless = 0
            print("you clawed it")
        else:
            self.bless += 16
            print("sorry, clawed nothing")
        

def main():
    signal.alarm(600)
    cc = ClawCrane()
    for _ in range(256):
        try:
            cc.run()
            print(f"your score: {cc.score}")
        except:
            print(f"abort")
            break
    if cc.score >= 2220:
        print(f"flag: {open('/flag.txt').read()}")
        
if __name__ == "__main__":
    main()