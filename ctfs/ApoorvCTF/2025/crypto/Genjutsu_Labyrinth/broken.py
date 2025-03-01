from sympy import primerange
import random
from collections import deque

def generate(size):
    grid = [[random.randint(0, 9) for col in range(size)] for row in range(size)]
    grid[0][0] = 0
    return grid

def encrypt(n, a, b, mod=101):
    return (a * n + b) % mod

def build_encrypted_grid(grid, a, b, mod=101):
    size = 10
    encry_grid = []
    for y in range(size):
        row = []
        for x in range(size):
            enc_val = encrypt(grid[y][x], a, b, mod)
            row.append(str(enc_val).zfill(2))
        encry_grid.append(row)
    return encry_grid

def optimize(grid):
    #hidden
    pass

grid = generate(10)
a = random.choice(list(primerange(2, 12)))
b = random.choice(range(101))
encry_grid = build_encrypted_grid(grid, a, b, mod=101)
