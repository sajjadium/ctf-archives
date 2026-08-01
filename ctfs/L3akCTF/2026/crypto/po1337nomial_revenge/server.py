#!/usr/bin/env python3

# Based on "po1337nomial" from Crew CTF 2025 - see https://7rocky.github.io/en/ctf/other/crewctf/po1337nomial/

from os import getenv
from random import getrandbits, randbytes, randrange, shuffle


FLAG = getenv('FLAG', 'L3AK{fake_flag}')

a = [getrandbits(32) for _ in range(1337)]
options = {'1': 'Get coefficients', '2': 'Evaluate', '3': 'Unlock flag'}

while options:
    option = input(''.join(f'\n{k}. {v}' for k, v in options.items()) + '\n> ')

    if option not in options:
        break

    options.pop(option)

    if option == '1':
        shuffle(s := a.copy())
        print('s:', s)

    if option == '2':
        x = int(input('x: '))
        a[randrange(0, 1337)] = 1337
        print('y:', 'REDACTED')

    if option == '3':
        if input('k: ') == randbytes(1337).hex():
            print(FLAG)
