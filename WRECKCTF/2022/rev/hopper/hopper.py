#!/usr/local/bin/python

import os


def do_hop(state):
    hopper = state['hopper']
    line = state['line']

    hops = [
        (hopper - 4, hopper >= 4),
        (hopper - 1, hopper % 4 != 0),
        (hopper + 1, hopper % 4 != 3),
        (hopper + 4, hopper < 12),
    ]

    hoppees = { line[hop]: hop for hop, legal in hops if legal }
    people = ', '.join(hoppees)

    print('oh no! the order of the line is wrong!')
    print(f'you can hop with {people}.')
    hoppee = input('who do you choose? ')

    if hoppee not in hoppees:
        print('can\'t hop there!')
        return

    target = hoppees[hoppee]
    line[hopper], line[target] = line[target], line[hopper]
    state['hopper'] = target


def fixed(state):
    position = { hoppee: i for i, hoppee in enumerate(state['line']) }
    if position['olive'] > position['olen']:
        return False
    if position['shauna'] > position['constance']:
        return False
    if position['zane'] > position['tracie']:
        return False
    if position['loretta'] > position['chasity']:
        return False
    if position['gracie'] > position['shauna']:
        return False
    if position['tracie'] > position['louie']:
        return False
    if position['bertram'] > position['antoinette']:
        return False
    if position['antoinette'] > position['dana']:
        return False
    if position['constance'] > position['bertram']:
        return False
    if position['louie'] > position['wes']:
        return False
    if position['olen'] > position['hopper']:
        return False
    if position['wes'] > position['loretta']:
        return False
    if position['chasity'] > position['olive']:
        return False
    if position['rosemarie'] > position['gracie']:
        return False
    if position['dana'] > position['zane']:
        return False
    return True


state = {
    'hopper': 0,
    'line': [
        'hopper',
        'wes',
        'gracie',
        'zane',
        'constance',
        'rosemarie',
        'shauna',
        'chasity',
        'louie',
        'tracie',
        'dana',
        'olen',
        'olive',
        'loretta',
        'bertram',
        'antoinette',
    ],
}

while not fixed(state):
    do_hop(state)

print(os.environ.get('FLAG', 'no flag provided!'))
