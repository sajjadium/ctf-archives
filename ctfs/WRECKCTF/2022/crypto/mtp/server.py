#!/usr/local/bin/python -u

import os
import random

LETTERS = set('abcdefghijklmnopqrstuvwxyz')


def encrypt(plaintext, key):
    return ''.join(
        chr(permutation[ord(letter) - ord('a')] + ord('a'))
        if letter in LETTERS
        else letter
        for letter, permutation in zip(plaintext, key)
    )


key = [list(range(26)) for _ in range(256)]
for permutation in key:
    random.shuffle(permutation)


print('Welcome to the Multi-Time Pad!')
while True:
    print('1. Encrypt message')
    print('2. Get flag')
    choice = input('> ')
    match choice:
        case '1':
            plaintext = input('What\'s your message? ')
        case '2':
            plaintext = os.environ.get('FLAG', 'no flag provided!')
        case _:
            print('Invalid choice!')
            continue
    print(f'Result: {encrypt(plaintext, key)}')
