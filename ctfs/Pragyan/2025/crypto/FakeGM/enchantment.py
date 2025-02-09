#!/usr/bin/env python3
import random
from random import randint
from sympy.functions.combinatorial.numbers import legendre_symbol
from math import gcd
from sympy import isprime, nextprime
from Crypto.Util.number import getPrime, bytes_to_long
from secrets import randbits
from random import getrandbits
import random
from dotenv import load_dotenv
import os
import time
from decimal import Decimal, getcontext

flag = open('flag.txt', 'rb').read().strip()

def brew_scrolls(seed, output_scroll,num_initial=719,num_predict=48):
    random.seed(seed)

    with open(output_scroll, 'w') as file:
        for index in range(num_initial):
            value = random.getrandbits(32)  
            unix_time = int(time.time())
            event="void"
            file.write(f"[{bin(index)[2:].zfill(10)}:{event}:{value}:{unix_time}]\n")

    values = [random.getrandbits(32) for _ in range(num_predict)]
    vtstr=""
    for index, val in enumerate(values, start=1):
        vstr=str(val)
        vtstr=vtstr+vstr
    fn=random.getrandbits(32)
    fne=str(fn)[:-2]
    vtstr+=fne
    return vtstr[:-9]

def run_process():
    load_dotenv()
    seed = os.getenv("SEED")

    if seed is None:
        raise ValueError("Seed is not set")
    
    output_scroll = 'scroll.log'
    result = int(brew_scrolls(seed, output_scroll))
    return result
    
result = run_process()

def brew_primes(bitL):
    while True:
        num1 = result
        num2 = randbits(512)

        p = (num1<<512)+ num2

        if isprime(p):
            return num1, num2, p

bitL = 2025
while 2025:
    q=randbits(2025)
    if isprime(q):
        break
num1, num2, p = brew_primes(bitL)

n=p*q

x = randint(2025, n) 
while 2025:
    lp = legendre_symbol(x, p)
    lq = legendre_symbol(x, q)
    if lp * lq > 0 and lp + lq < 0:
        break
    x = randint(2025, n)

m = map(int, bin(bytes_to_long(flag))[2:])

binary_list = list(m)  

c = []
for b in binary_list:
    while 2025:
        r = randint(2025, n)
        if gcd(r, n) == 1:
            break
    c.append((pow(x, 2025 + b, n) * pow(r, 2025+2025, n)) % n)

with open("scroll.txt", "w") as outfile:
    outfile.write(f"n = {n}\n")
    outfile.write(f"c = {c}\n")

