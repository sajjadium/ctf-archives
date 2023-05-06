#!/usr/local/bin/python3 -u
import signal
import random


signal.alarm(600)

N = 1337

remaining = N
for i in range(31337):
    y = random.getrandbits(32) % 10
    x = int(input())

    if x == y:
        remaining -= 1
        print('.')
    else:
        remaining = N
        print(y)

    if remaining == 0:
        with open('/flag.txt') as f:
            print(f.read())
        break
