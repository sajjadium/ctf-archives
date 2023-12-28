#!/usr/bin/env python3
# Adapted from https://github.com/balsn/proof-of-work
import hashlib
import sys
import requests


def is_valid(digest, zeros, difficulty):
    if sys.version_info.major == 2:
        digest = [ord(i) for i in digest]
    bits = ''.join(bin(i)[2:].zfill(8) for i in digest)
    return bits[:difficulty] == zeros


if __name__ == '__main__':
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    else:
        HOST = 'http://challenge17.play.potluckctf.com:31337'

    info = requests.post(f'{HOST}/pow', json={}).json()
    prefix = info['prefix']
    difficulty = info['difficulty']

    print(f'prefix: {prefix}')
    print(f'difficulty: {difficulty}')

    zeros = '0' * difficulty
    i = 0
    while True:
        i += 1
        s = prefix + str(i)
        if is_valid(hashlib.sha256(s.encode()).digest(), zeros, difficulty):
            info = requests.post(f'{HOST}/pow', json={
                'prefix': prefix,
                'answer': str(i)
            }).json()
            print('Token: ' + info['token'])
            exit(0)
