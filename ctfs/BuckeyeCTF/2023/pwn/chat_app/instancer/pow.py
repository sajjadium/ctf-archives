#!/usr/bin/env python3

# This is from kCTF (modified to remove backdoor)
# https://github.com/google/kctf/blob/69bf578e1275c9223606ab6f0eb1e69c51d0c688/docker-images/challenge/pow.py

# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os
import secrets
import socket
import sys
import hashlib

try:
    import gmpy2
    HAVE_GMP = True
except ImportError:
    HAVE_GMP = False
    sys.stderr.write("[NOTICE] Running 10x slower, gotta go fast? pip3 install gmpy2\n")

VERSION = 's'
MODULUS = 2**1279-1
CHALSIZE = 2**128

SOLVER_URL = 'https://goo.gle/kctf-pow'

def python_sloth_root(x, diff, p):
    exponent = (p + 1) // 4
    for i in range(diff):
        x = pow(x, exponent, p) ^ 1
    return x

def python_sloth_square(y, diff, p):
    for i in range(diff):
        y = pow(y ^ 1, 2, p)
    return y

def gmpy_sloth_root(x, diff, p):
    exponent = (p + 1) // 4
    for i in range(diff):
        x = gmpy2.powmod(x, exponent, p).bit_flip(0)
    return int(x)

def gmpy_sloth_square(y, diff, p):
    y = gmpy2.mpz(y)
    for i in range(diff):
        y = gmpy2.powmod(y.bit_flip(0), 2, p)
    return int(y)

def sloth_root(x, diff, p):
    if HAVE_GMP:
        return gmpy_sloth_root(x, diff, p)
    else:
        return python_sloth_root(x, diff, p)

def sloth_square(x, diff, p):
    if HAVE_GMP:
        return gmpy_sloth_square(x, diff, p)
    else:
        return python_sloth_square(x, diff, p)

def encode_number(num):
    size = (num.bit_length() // 24) * 3 + 3
    return str(base64.b64encode(num.to_bytes(size, 'big')), 'utf-8')

def decode_number(enc):
    return int.from_bytes(base64.b64decode(bytes(enc, 'utf-8')), 'big')

def decode_challenge(enc):
    dec = enc.split('.')
    if dec[0] != VERSION:
        raise Exception('Unknown challenge version')
    return list(map(decode_number, dec[1:]))

def encode_challenge(arr):
    return '.'.join([VERSION] + list(map(encode_number, arr)))

def get_challenge(diff):
    x = secrets.randbelow(CHALSIZE)
    return encode_challenge([diff, x])

def solve_challenge(chal):
    [diff, x] = decode_challenge(chal)
    y = sloth_root(x, diff, MODULUS)
    return encode_challenge([y])

def verify_challenge(chal, sol):
    [diff, x] = decode_challenge(chal)
    [y] = decode_challenge(sol)
    res = sloth_square(y, diff, MODULUS)
    return (x == res) or (MODULUS - x == res)

def usage():
    sys.stdout.write('Usage:\n')
    sys.stdout.write('Solve pow: {} solve $challenge\n')
    sys.stdout.write('Check pow: {} ask $difficulty\n')
    sys.stdout.write('  $difficulty examples (for 1.6GHz CPU) in fast mode:\n')
    sys.stdout.write('             1337:   1 sec\n')
    sys.stdout.write('             31337:  30 secs\n')
    sys.stdout.write('             313373: 5 mins\n')
    sys.stdout.flush()
    sys.exit(1)

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'ask':
        difficulty = int(sys.argv[2])

        if difficulty == 0:
            sys.stdout.write("== proof-of-work: disabled ==\n")
            sys.exit(0)


        challenge = get_challenge(difficulty)

        sys.stdout.write("== proof-of-work: enabled ==\n")
        sys.stdout.write("please solve a pow first\n")
        sys.stdout.write("You can run the solver with:\n")
        sys.stdout.write("    python3 <(curl -sSL {}) solve {}\n".format(SOLVER_URL, challenge))
        sys.stdout.write("===================\n")
        sys.stdout.write("\n")
        sys.stdout.write("Solution? ")
        sys.stdout.flush()
        solution = ''
        with os.fdopen(0, "rb", 0) as f:
            while not solution:
                line = f.readline().decode("utf-8")
                if not line:
                    sys.stdout.write("EOF")
                    sys.stdout.flush()
                    sys.exit(1)
                solution = line.strip()

        if verify_challenge(challenge, solution):
            sys.stdout.write("Correct\n")
            sys.stdout.flush()
            sys.exit(0)
        else:
            sys.stdout.write("Proof-of-work fail")
            sys.stdout.flush()

    elif cmd == 'solve':
        challenge = sys.argv[2]
        solution = solve_challenge(challenge)

        if verify_challenge(challenge, solution, False):
            sys.stderr.write("Solution: \n".format(solution))
            sys.stderr.flush()
            sys.stdout.write(solution)
            sys.stdout.flush()
            sys.stderr.write("\n")
            sys.stderr.flush()
            sys.exit(0)
    else:
        usage()

    sys.exit(1)

if __name__ == "__main__":
    main()