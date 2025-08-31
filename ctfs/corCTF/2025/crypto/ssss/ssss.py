#!/usr/local/bin/python3
import random

p = 2**255 - 19
k = 15
SECRET = random.randrange(0, p)

print("welcome to ssss")
# Step 1: Generate a random, degree-(k−3) polynomial g(x)
g = [random.randrange(p) for _ in range(k - 2)]
# Step 2: Select a random c in Fp
c = random.randrange(0, p)
# Step 3: Set f(x)=g(x)x^2+Sx+c
f = [c] + [SECRET] + g

def evaluate_poly(f, x):
    return sum(c * pow(x, i, p) for i, c in enumerate(f)) % p

for _ in range(k - 1):
    x = int(input())
    assert 0 < x < p, "no cheating!"
    print(evaluate_poly(f, x))

if int(input("secret? ")) == SECRET:
    FLAG = open("flag.txt").read()
    print(FLAG)