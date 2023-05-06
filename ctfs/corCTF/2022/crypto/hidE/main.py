#!/usr/local/bin/python
import random
import time
import math
import binascii
from Crypto.Util.number import *

p, q = getPrime(512), getPrime(512)
n = p * q
phi = (p - 1) * (q - 1)

flag = open('./flag.txt').read().encode()

random.seed(int(time.time()))

def encrypt(msg):
    e = random.randint(1, n)
    while math.gcd(e, phi) != 1:
        e = random.randint(1, n)
    pt = bytes_to_long(msg)
    ct = pow(pt, e, n)
    return binascii.hexlify(long_to_bytes(ct)).decode()


def main():
    print('Secure Encryption Service')
    print('Your modulus is:', n)
    while True:
        print('Options')
        print('-------')
        print('(1) Encrypt flag')
        print('(2) Encrypt message')
        print('(3) Quit')
        x = input('Choose an option: ')
        if x not in '123':
            print('Unrecognized option.')
            exit()
        elif x == '1':
            print('Here is your encrypted flag:', encrypt(flag))
        elif x == '2':
            msg = input('Enter your message in hex: ')
            print('Here is your encrypted message:', encrypt(binascii.unhexlify(msg)))
        elif x == '3':
            print('Bye')
            exit()

if __name__ == '__main__':
    main()
