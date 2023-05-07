from Crypto.Util.number import *
from math import gcd
from secret import flag
import random

NBITS = 32

print("=== Knapsack vs. Backpack ===")

class Knapsack:
    def __init__(self, nbits):
        W, P = [], []
        for _ in range(nbits):
            W.append(random.randint(1, 10))
            P.append(random.randint(1, 100))
        
        self.W, self.P = W, P

    def fill(self, nbits):
        r = getRandomNBitInteger(nbits)
        pt = [int(i) for i in bin(r)[2:].zfill(nbits)]
        self.A = sum([x * y for x, y in zip(pt, self.W)])
        self.B = sum([x * y for x, y in zip(pt, self.P)])

try:
    for _ in range(10):
        challenge1 = Knapsack(NBITS*4)
        challenge1.fill(NBITS*4)
        print(challenge1.W)
        print(challenge1.P)
        print(f"Knapsack Capacity: {challenge1.A}")

        inp = list(map(int, input("Items: ").strip().split()))
        for i in inp:
            if i < 0 or i >= len(challenge1.W):
                print("Nope.")
                exit(1)
        if len(inp) != len(set(inp)):
            print("Nope.")
            exit(1)
        weight = sum([challenge1.W[i] for i in inp])
        profit = sum([challenge1.P[i] for i in inp])
        if weight <= challenge1.A and profit >= challenge1.B:
            print("Correct!")
        else:
            print("Nope.")
            exit(1)
except:
    exit(1)

print(flag[:len(flag)//2])

class Backpack:
    def __init__(self, nbits):
        r = [42]
        for _ in range(nbits - 1):
            r.append(random.randint(2*r[-1], 4*r[-1]))
        
        B = random.randint(3*r[-1] + 1, 4*r[-1])
        A = random.randint(2*r[-1] + 1, B - 1)
        while gcd(A, B) != 1:
            A = random.randint(2*r[-1] + 1, B - 1)

        self.M = [A * _ % B for _ in r]

    def fill(self, inp):
        return sum([x * y for x, y in zip(inp, self.M)])

try:
    for _ in range(10):
        challenge2 = Backpack(NBITS)
        r = getRandomNBitInteger(NBITS)
        pt = [int(i) for i in bin(r)[2:].zfill(NBITS)]
        ct = challenge2.fill(pt)
        print(challenge2.M)
        print(f"In your Knapsack: {ct}")

        inp = int(input("Secret: ").strip())
        if inp == r:
            print("Correct!")
        else:
            print("Nope.")
            exit(1)
except:
    exit(1)

print(flag[len(flag)//2:])