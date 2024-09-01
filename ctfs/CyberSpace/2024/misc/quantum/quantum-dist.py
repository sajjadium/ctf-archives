# We ran this challenge on a quantum computer
FLAG = "CSCTF{fake_flag_for_testing}"

import random


def gen(mn, mx):
    n = random.randint(mn, mx)
    global p
    p = [0] * n
    for i in range(n):
        p[i] = (random.randint(1, n), random.randint(1, n))
    return p


def ask(x0, y0):
    sum = 0
    for x, y in p:
        sum += abs(x - x0) + abs(y - y0)
    return sum


def query(x0, y0, x1, y1):
    sum = 0
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            sum += ask(x, y)
    return sum
