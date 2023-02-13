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

fakeflag = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(13)]) + "}"
fakeflag2 = "lactf{" + ''.join([chr(ord('a')+np.random.randint(0,26)) for _ in range(13)]) + "}"
assert(len(fakeflag) == n)
assert(len(fakeflag2) == n)
f = encrypt(fakeflag)
f2 = encrypt(fakeflag2)

def xorencrypt(s):
    v1 = stov(s)
    v2 = stov(fakeflag)
    v = np.bitwise_xor(v1, v2)
    return encrypt(vtos(v))

def giveflag():
    flag = open("flag.txt", "r").readline().strip()
    print("\nYour vision fades to black, and arcane symbols begin to swarm your mind. To others, it might seem like magic, but you can see what others cannot.")
    print(flag)
    exit(0)

def oracle(guess):
    print(xorencrypt(guess))

def trydecode():
    guess = input("\nEnter your guess: ")
    if len(guess) != 20:
        return 1
    for c in guess:
        if ord(c) < 32 or ord(c) >= 127:
            return 2
        if c == ' ':
            return 3
    
    oracle(guess)
    return 0

def guess(num):
    while (err := trydecode()) != 0:
        if err == 1:
            print("Your guess must be exactly 20 characters.")
        elif err == 2:
            print("Your guess must use only ASCII characters")
        elif err == 3:
            print("Sorry, spaces aren't allowed anymore.")
    
    print("You have", 13-num, "attempts left")

print("On the hill lies a stone. It reads:")
print(f)
print("\nA mysterious figure offers you 14 uses of an oracle:")
for i in range(14):
    guess(i)

print("\nThe figure vanishes, leaving only a vague message. Encrypt me:")
print(fakeflag2)
guess = input("\nEnter your guess: ")
if guess == f2:
    giveflag()
else:
    print("Nope.")
