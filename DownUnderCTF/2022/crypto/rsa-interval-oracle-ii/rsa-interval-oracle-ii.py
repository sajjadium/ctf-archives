#!/usr/bin/env python3

import signal, time
from os import urandom, path
from Crypto.Util.number import getPrime, bytes_to_long


FLAG = open(path.join(path.dirname(__file__), 'flag.txt'), 'r').read().strip()

N_BITS = 384
TIMEOUT = 20 * 60
MAX_INTERVALS = 1
MAX_QUERIES = 384


def main():
    p, q = getPrime(N_BITS//2), getPrime(N_BITS//2)
    N = p * q
    e = 0x10001
    d = pow(e, -1, (p - 1) * (q - 1))

    secret = bytes_to_long(urandom(N_BITS//9))
    c = pow(secret, e, N)

    print(N)
    print(c)

    intervals = []
    queries_used = 0

    while True:
        print('1. Add interval\n2. Request oracle\n3. Get flag')
        choice = int(input('> '))

        if choice == 1:
            if len(intervals) >= MAX_INTERVALS:
                print('No more intervals allowed!')
                continue

            lower = int(input(f'Lower bound: '))
            upper = int(input(f'Upper bound: '))
            intervals.insert(0, (lower, upper))

        elif choice == 2:
            queries = input('queries: ')
            queries = [int(c.strip()) for c in queries.split(',')]
            queries_used += len(queries)
            if queries_used > MAX_QUERIES:
                print('No more queries allowed!')
                continue

            results = []
            for c in queries:
                m = pow(c, d, N)
                for i, (lower, upper) in enumerate(intervals):
                    in_interval = lower < m < upper
                    if in_interval:
                        results.append(i)
                        break
                else:
                    results.append(-1)

            print(','.join(map(str, results)), flush=True)

            time.sleep(MAX_INTERVALS * (MAX_QUERIES // N_BITS - 1))
        elif choice == 3:
            secret_guess = int(input('Enter secret: '))
            if secret == secret_guess:
                print(FLAG)
            else:
                print('Incorrect secret :(')
            exit()

        else:
            print('Invalid choice')


if __name__ == '__main__':
    signal.alarm(TIMEOUT)
    main()
