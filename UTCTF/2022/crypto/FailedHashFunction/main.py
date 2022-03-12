#!/usr/bin/env python3
import sys, os

def trailing(x):
    a = 0
    for _ in range(15):
        if x & 1:
            break
        x >>= 1
        a += 1
    return a

def print_hash(s):
    for x in s:
        for y in s:
            print(hex(trailing((k1 ^ x) * (k2 ^ y)))[2:], end='')
    print()

for num in range(1,101):
    print('Challenge', num)
    k1 = os.urandom(1)[0]
    k2 = os.urandom(1)[0]

    print('Enter 16 bytes to hash! You only get two tries ;)')
    s = sys.stdin.buffer.read(16)
    print_hash(s)
    

    print('Enter 16 bytes to hash! Last chance...')
    s = sys.stdin.buffer.read(16)
    print_hash(s)

    print('Time to guess >:)')
    print('k1:')
    a = int(input())
    print('k2:')
    b = int(input())

    if not (a == k1 and b == k2 or a == k2 and b == k1):
        print("Oops you're wrong :(")
        exit(0)

print("Dang... guess it really is broken :(")

with open("flag.txt") as f:
    print(f.read())
    
