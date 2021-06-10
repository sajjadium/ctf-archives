#!/usr/bin/env python
import sys
import string
import random
import md5
import re

alpha = string.lowercase + string.uppercase + string.digits

def rand_string(length):
    return ''.join([random.choice(alpha) for _ in range(length)])

def check(inp, prefix):
    if not re.match('^[a-zA-Z0-9]+$', inp):
        return False

    digest = md5.new(inp).digest()
    return prefix == digest[:len(prefix)]

def ask(difficulty):
    prefix = rand_string(difficulty)
    print('Proof of work challenge:'.format(difficulty, prefix))
    print('md5([a-zA-Z0-9]+)[:{}] == {}'.format(difficulty, prefix))
    print('Input: ')
    inp = raw_input().strip()

    if check(inp, prefix):
        print('Correct :)')
        exit(2)
    else:
        print('Incorrect :(')

def solve(prefix):
    while True:
        attempt = rand_string(5)
        if check(attempt, prefix):
            print('Solution: {}'.format(attempt))

if __name__=='__main__':
    if len(sys.argv) < 3:
        print('use "ask <difficulty>" or "solve <prefix>"')
    elif sys.argv[1] == 'ask':
        ask(int(sys.argv[2]))
    elif sys.argv[1] == 'solve':
        solve(sys.argv[2])

