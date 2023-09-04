#!/usr/bin/env python3

import sys
import tempfile
import os


def main():
    print('V8 version 11.6.205')
    print('> ', end='')
    sys.stdout.flush()

    data = sys.stdin.readline().encode()

    with tempfile.NamedTemporaryFile() as f:
        f.write(data)
        f.flush()
        os.system(f'./d8 {f.name}')


if __name__ == '__main__':
    main()

