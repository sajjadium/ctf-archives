#!/usr/local/bin/python3.10 -u

import ast
import sys

import select
from Crypto.Util import number
import hashlib

with open('flag.txt') as f:
    flag = f.readline()

raw_bin = str(
    bin(int('0x'+str(hashlib.sha256(flag.encode('utf-8')).hexdigest()), 16))[2:])
hsh = int('0b1' + '0' * (256 - len(raw_bin)) + raw_bin, 2)

p = number.getPrime(1024)
q = number.getPrime(1024)
n = p * q
e = 0

for i in range(0, 100):
    if pow(hsh, i) >= n:
        e = i
        break

m = pow(hsh, e, n)
print(f'm: {m}')
print(f'n: {n}')


def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    raise Exception


try:
    answer = input_with_timeout('', 20)
    try:
        answer = ast.literal_eval(answer)
        if hsh == answer:
            print('you love rsa so i <3 you :DD')
            print(flag)
        else:
            print("im upset")
    except Exception as e:
        print("im very upset")
except Exception as e:
    print("\nyou've let me down :(")
