#!/usr/bin/env python3
import random
import math
import time
import binascii

p = 2**135 + 2**75 + 1
a = 313370
b = 12409401451673702436179381616844751057480 # discriminant is zero
g = (313379, 9762458732130899649993884045943131856797, False) 

def negp(P):
    x,y,z = P
    return (-x,y,z)

def dubp(P):
    x,y,z = P
    if z:
        return P
    if y == 0:
        return (0, 0, True)
    L = (3 * x * x + a) * pow(2 * y, -1, p)
    xr = L * L - 2 * x
    yr = y + L * (xr - x)
    return (xr % p, -yr % p, False)

def addp(P, Q):
    xp,yp,zp = P
    xq,yq,zq = Q
    if zp:
        return Q
    if zq:
        return P
    if P == negp(Q):
        return (0, 0, True)
    if P == Q:
        return dubp(P)
    L = (yq - yp) * pow(xq - xp, -1, p)
    xr = L*L - xp - xq
    yr = yp + L * (xr - xp)
    return (xr % p, -yr % p, False)

def mulp(P, n):
    s = bin(n)[3:]
    r = P
    for c in s:
        r = dubp(r)
        if c == '1':
            r = addp(r, P)
    return r

print("""
Welcome to the final iteration of FNES.
The purpose of FNES is now to generate a shared secret using input from both parties.
Here are the steps:
1. Friends A and B both launch FNES 3
2. A and B follow the instructions to generate a shared secret
3. A and B can now pass messages back and forth as normal
No more unencryptable characters, but you need to make sure to
not make any mistakes or your keystreams can come out of sync.
""", flush=True)

print("Are you friend A or friend B?", flush=True)
l = input(">>> ").strip().upper()
if (len(l) > 1):
    print("You inputted more than one character...", flush=True)
elif (l == "A"):
    print("Please enter a large random number to use as your secret key.", flush=True)
    aa = int(input(">>> ").strip())
    A = mulp(g, aa)
    if (A[2]):
        print("That didn't work. Try again with a different key.", flush=True)
        exit()
    print(f"Your public key is x={A[0]}, y={A[1]}. \nSend this to B. \nWhat is their public key?", flush=True)
    B = (int(input(">>> x = ").strip()), int(input(">>> y = ").strip()), False)
    S = mulp(B, aa)
    random.seed(S[0] + S[1])
    print("Seeding complete.", flush=True)
elif (l == "B"):
    print("Please enter a large random number to use as your secret key.", flush=True)
    aa = int(input(">>> ").strip())
    A = mulp(g, aa)
    if (A[2]):
        print("That didn't work. Try again with a different key.", flush=True)
        exit()
    print("What is A's public key?", flush=True)
    B = (int(input(">>> x = ").strip()), int(input(">>> y = ").strip()), False)
    S = mulp(B, aa)
    random.seed(S[0] + S[1])
    print(f"Your public key is x={A[0]}, y={A[1]}. \nSend this to A.", flush=True)
    print("Seeding complete.", flush=True)
else:
    print("That's not A or B!", flush=True)
    exit()

while True:
    print("Would you like to encrypt (E), decrypt (D), or quit (Q)?", flush=True)
    l = input(">>> ").strip().upper()
    if (len(l) > 1):
        print("You inputted more than one character...", flush=True)
    elif (l == "Q"):
        print("We hope you enjoyed!", flush=True)
        exit()
    elif (l == "E"):
        print("What would you like to encrypt?", flush=True)
        I = str.encode(input(">>> ").strip())
        print("Here's your message:", flush=True)
        i = int(binascii.hexlify(I), 16)
        i ^= random.getrandbits(len(I) * 8)
        i = hex(i)[2:]
        if len(i) % 2 == 1:
            i = '0' + i
        print(i, flush=True)
    elif (l == "D"):
        print("What was the message?", flush=True)
        I = input(">>> ").strip()
        try:
            m = int(I, 16)
            m ^= random.getrandbits(4 * len(I))
            m = str(binascii.unhexlify(hex(m)[2:]))[2:-1]
            print("Here's the decoded message:", flush=True)
            print(m, flush=True)
        except ValueError:
            print("I can't read that!", flush=True)

