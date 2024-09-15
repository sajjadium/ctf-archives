#!/usr/bin/env python3

from random import SystemRandom
import os

random = SystemRandom()

p = 241
SB = [31, 32, 57, 9, 31, 144, 126, 114, 1, 38, 231, 220, 122, 169, 105, 29, 33, 81, 129, 4, 6, 64, 97, 134, 193, 160, 150, 145, 114, 133, 23, 193, 73, 162, 220, 111, 164, 88, 56, 102, 0, 107, 37, 227, 129, 17, 143, 134, 76, 152, 39, 233, 0, 147, 9, 220, 182, 113, 203, 11, 31, 125, 125, 194, 223, 192, 49, 71, 20, 227, 25, 38, 132, 17, 90, 109, 36, 157, 238, 127, 115, 92, 149, 216, 182, 15, 123, 28, 173, 114, 86, 159, 117, 60, 42, 191, 106, 182, 43, 108, 24, 232, 159, 25, 240, 78, 207, 158, 132, 156, 203, 71, 226, 235, 91, 92, 238, 110, 195, 78, 8, 54, 225, 108, 193, 65, 211, 212, 68, 77, 232, 100, 147, 171, 145, 96, 225, 63, 37, 144, 71, 38, 195, 19, 121, 197, 112, 20, 2, 186, 144, 217, 189, 130, 34, 180, 47, 121, 87, 154, 211, 188, 176, 65, 146, 26, 194, 213, 45, 171, 24, 37, 76, 42, 232, 13, 111, 80, 109, 178, 178, 31, 51, 100, 190, 121, 83, 53, 156, 62, 70, 23, 151, 227, 169, 160, 45, 174, 76, 25, 196, 62, 201, 6, 215, 139, 192, 83, 141, 230, 110, 39, 170, 189, 158, 153, 143, 110, 169, 206, 239, 56, 58, 174, 222, 29, 33, 198, 134, 181, 83, 72, 24, 61, 189, 177, 159, 31, 53, 5, 30]
state_size = 32
r = 16
c = state_size - r
ROUNDS = 140
rc = [0 for i in range(ROUNDS)]
start_state = [0]*state_size

flag = os.environ.get("FLAG", "ptm{REDACTED}")

def absorb(state):
    state = state[:]
    for i in range(ROUNDS):
        tmp = SB[(state[0] + rc[i]) % p]
        for j in range(1, len(state)):
            state[j] += tmp
            state[j] %= p
        state = state[1:] + state[:1]
    return state

def sponge(payload):
    assert len(payload) % r == 0
    state = start_state[:]
    for i in range(0, len(payload), r):
        state = [(state[j] + payload[i+j]) % p for j in range(r)] + state[r:]
        state = absorb(state)
    return state[:r-4]

def h(msg):
    m = msg[:]
    m.append(len(m))
    if len(m) % r != 0:
        m += [0] * (r - (len(m) % r))
    return sponge(m) 

for i in range(10):
    rc = [random.randint(1,p-1) for i in range(ROUNDS)]

    print(f"Iteration {i+1}")
    print(f"{rc = }")
    m1 = list(bytes.fromhex(input("M1: ")))
    m2 = list(bytes.fromhex(input("M2: ")))

    if m1 == m2 or h(m1) != h(m2) or any([x>=p for x in m1]) or any([x>=p for x in m2]) or len(m1)>=p or len(m2)>=p:
        print("Nope!", m1, m2, h(m1), h(m2))
        exit()

print(flag)