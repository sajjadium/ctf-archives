from random import randint
from math import gcd, log
import time
from Crypto.Util.number import *


def check(n, iterations=50):
    if isPrime(n):
        return False

    i = 0
    while i < iterations:
        a = randint(2, n - 1)
        if gcd(a, n) == 1:
            i += 1
            if pow(a, n - 1, n) != 1:
                return False
    return True


def generate_challenge(c):
    a = randint(2, c - 1)
    while gcd(a, c) != 1:
        a = randint(2, c - 1)
    k = randint(2, c - 1)
    return (a, pow(a, k, c))


def get_flag():
    with open('flag.txt', 'r') as f:
        return f.read()

if __name__ == '__main__':
    c = int(input('c = '))

    if log(c, 2) < 512:
        print(f'c must be least 512 bits large.')
    elif not check(c):
        print(f'No cheating!')
    else:
        a, b = generate_challenge(c)
        print(f'a = {a}')
        print(f'a^k = {b} (mod c)')
        
        k = int(input('k = '))

        if pow(a, k, c) == b:
            print(get_flag())
        else:
            print('Wrong k')
        
