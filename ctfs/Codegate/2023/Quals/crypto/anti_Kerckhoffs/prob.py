import math
import os
import hashlib
import signal
import secrets

QUERY_LIMIT = 77777
MOD = 17
m = 20

def quadratic_eval(coeffs, x):
    return (coeffs[2] * x ** 2 + coeffs[1] * x + coeffs[0]) % MOD

def get_random_quadratic():
    c2 = secrets.randbelow(MOD - 1) + 1
    c1 = secrets.randbelow(MOD)
    c0 = secrets.randbelow(MOD)
    return [c0, c1, c2]

def calc(Inputs):
    Outputs = [quadratic_eval(SboxLayer1[i], Inputs[i]) for i in range(m)]
    Outputs = [sum(LinearLayer[i][j] * Outputs[j] for j in range(m)) for i in range(m)]
    Outputs = [quadratic_eval(SboxLayer2[i], Outputs[i]) for i in range(m)]
    return Outputs

def print_list(L, prefix = ''):
    print(prefix, end='')
    for x in L:
        print(x, end = ' ')
    print()

def compare(L1, L2):
    ret = 0
    for i in range(m):
        if L1[i] == L2[i]:
            ret += 2 ** i
    return ret

def list_to_int(L):
    assert len(L) == m, "Invalid list format"
    assert all(0 <= x < MOD for x in L), "Invalid list format"
    ret = 0
    for i in range(m):
        ret += L[i] * MOD ** i
    return ret

def int_to_list(x):
    assert 0 <= x < MOD ** m, "Invalid int format"
    L = [0] * m
    for i in range(m):
        L[i] = x % MOD
        x //= MOD
    return L

SboxLayer1 = [get_random_quadratic() for _ in range(m)]
LinearLayer = [[secrets.randbelow(MOD-1) + 1 for _ in range(m)] for _ in range(m)]
SboxLayer2 = [get_random_quadratic() for _ in range(m)]

HIDDEN = [secrets.randbelow(MOD) for _ in range(m)]
TARGET = calc(HIDDEN)

print(f"TARGET = {list_to_int(TARGET)}")

query_count = 0

win = False

while not win:
    Inputs = list(map(int, input("Inputs > ").split()))
    query_count += len(Inputs)
    if query_count > QUERY_LIMIT:
        print("bye..")
        exit(-1)
    Outputs = []
    
    for I in Inputs:
        O = calc(int_to_list(I))
        if TARGET == O:
            win = True
        Outputs.append(compare(TARGET, O))
    print_list(Outputs, "Outputs = ")

print("Good job!", open("flag", 'r').read())
        


