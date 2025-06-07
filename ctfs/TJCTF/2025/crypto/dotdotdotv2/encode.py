import numpy as np
import random
import sys

sys.stdin = open("flag.txt", "r")
sys.stdout = open("encoded.txt", "w")

n = 64

filler = "In cybersecurity, a CTF (Capture The Flag) challenge is a competitive, gamified event where participants, either individually or in teams, are tasked with finding and exploiting vulnerabilities in systems to capture hidden information known as flags. These flags are typically used to score points. CTFs test skills in areas like cryptography, web security, reverse engineering, and forensics, offering an exciting way to learn, practice, and showcase cybersecurity expertise.  This flag is for you: "

flag = input()
flag = filler+flag
flag = "".join([bin(ord(i))[2:].zfill(8) for i in flag])
flag = flag + "0"*(n-len(flag)%n)
flag = np.array([list(map(int,list(flag[i:i+n]))) for i in range(0, len(flag), n)])

key = np.array([[random.randint(0,0xdeadbeef) for _ in range(n)] for _ in range(n)])

for i in flag: print(*list(np.dot(i,key)))