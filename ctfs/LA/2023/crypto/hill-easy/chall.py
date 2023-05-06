#!/usr/local/bin/python3

import numpy as np

def det(M):
    # stolen from https://stackoverflow.com/a/66192895
    M = [[int(x) for x in row] for row in M] # make a copy to keep original M unmodified
    N, sign, prev = len(M), 1, 1
    for i in range(N-1):
        if M[i][i] == 0: # swap with another row having nonzero i's elem
            swapto = next( (j for j in range(i+1,N) if M[j][i] != 0), None )
            if swapto is None:
                return 0 # all M[*][i] are zero => zero determinant
            M[i], M[swapto], sign = M[swapto], M[i], -sign
        for j in range(i+1,N):
            for k in range(i+1,N):
                assert ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) % prev == 0
                M[j][k] = ( M[j][k] * M[i][i] - M[j][i] * M[i][k] ) // prev
        prev = M[i][i]
    return sign * M[-1][-1]

n = 20
A = np.random.randint(0, 95, [n, n])
while np.gcd(det(A), 95) != 1:
    # ensures invertibility
    A = np.random.randint(0, 95, [n, n])

def stov(s):
    return np.array([ord(c)-32 for c in s])

def vtos(v):
    return ''.join([chr(v[i]+32) for i in range(n)])

def encrypt(s):
    return vtos(np.matmul(A, stov(s))%95)

fakeflag = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(33)]) + "}"
fakeflag2 = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(33)]) + "}"
assert(len(fakeflag) == 2*n)
assert(len(fakeflag2) == 2*n)
f1 = encrypt(fakeflag[:n])
f2 = encrypt(fakeflag[n:])
f3 = encrypt(fakeflag2[:n])
f4 = encrypt(fakeflag2[n:])

def giveflag():
    flag = open("flag.txt", "r").readline().strip()
    print("\nThe text on the stone begins to rearrange itself into another message:")
    print(flag)
    exit(0)

def oracle(guess):
    o1 = encrypt(guess[:n])
    o2 = encrypt(guess[n:])
    if o1 == f1 and o2 == f2:
        giveflag()
    print("Incorrect:")
    print(o1)
    print(o2)

def trydecode():
    guess = input("\nEnter your guess: ")
    if len(guess) != 40:
        return 1
    for c in guess:
        if ord(c) < 32 or ord(c) >= 127:
            return 2
    
    oracle(guess)
    return 0

def guess(num):
    while (err := trydecode()) != 0:
        if err == 1:
            print("Your guess must be exactly 40 characters.")
        elif err == 2:
            print("Your guess must use only ASCII characters")
    
    print("You have", 9-num, "attempts left")

print("On the hill lies a stone. It reads:")
print(f1)
print(f2)
print("\nA mysterious figure offers you 10 attempts at decoding the stone:")
for i in range(10):
    guess(i)
print("\nThe figure frowns, and turns to leave. In desperation, you beg for one more chance. The figure ponders, then reluctantly agrees to offer you an alternative task.")
print("Create a new stone that decodes to the following:")
print(fakeflag2)
guess1 = input("\nEnter the first half: ")
guess2 = input("\nEnter the second half: ")
if guess1 == f3 and guess2 == f4:
    giveflag()
else:
    print("Nope.")
