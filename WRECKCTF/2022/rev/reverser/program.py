#!/usr/local/bin/python

import os

def check_license(license):
    characters = set('0123456789abcdef')
    s = [9]
    for c in license:
        if c not in characters:
            return False
        s.append((s[-1] + int(c, 16)) % 16)
    target = '51c49a1a00647b037f5f3d5c878eb656'
    return ''.join(f'{c:x}' for c in s[1:]) == target

print('welcome to reverser as a service!')
license = input('please enter your license key: ')

if not check_license(license):
    print('sorry, incorrect key!')
    exit()

string = input('what should i reverse? ')
print(f'output: {string[::-1]}')
print(os.environ.get('FLAG', 'no flag given'))
