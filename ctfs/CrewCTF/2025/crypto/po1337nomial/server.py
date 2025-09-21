#!/usr/bin/env python3

from os import getenv
from random import getrandbits, randbytes, randrange, shuffle


FLAG = getenv('FLAG', 'crew{fake_flag}')

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
        print('y:', sum(a_i * x ** i for i, a_i in enumerate(a)))

    if option == '3':
        if input('k: ') == randbytes(1337).hex():
            print(FLAG)
