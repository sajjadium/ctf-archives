#!/usr/bin/env python3

import math
import secrets

from Crypto.Util.number import * 

from redacted import FLAG

PM = 0.05

def genetic_prime_gen(target_size_bits):
    population = ['10', '11', '101']
    number_large = 0
    while True:
        a, b = secrets.choice(population), secrets.choice(population)
        # Crossover
        child = a + b
        if secrets.randbelow(100) < PM*100:
            # Mutation
            x = secrets.randbelow(len(child))
            child = child[:x] + ('1' if child[x] == '0' else '0') + child[x+1:]
        if isPrime(int(child, 2)) and child not in population:
            if len(child) > target_size_bits:
                number_large += 1
            population.append(child)
        if number_large >= 2:
            break
    population.sort(key=lambda x: len(x), reverse=True)
    return population[0], population[1]


for i in range(20):
    p, q = genetic_prime_gen(512)
    p = int(p, 2)
    q = int(q, 2)
    N = p*q
    e = 65537
    c = pow(bytes_to_long(FLAG), e, N)
    print(f'{N=}')    
    print(f'{e=}')    
    print(f'{c=}')    
    print()
