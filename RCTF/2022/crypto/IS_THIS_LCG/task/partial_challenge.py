"""
As we known, 
LCG state can be regained with some given output.
But this time we only give partial output each time!
"""
from sage.all import *
from Crypto.Util.number import bytes_to_long, getRandomInteger

def gen_p1():
    m = 2 ** 1024
    a = bytes_to_long(b'Welcome to RCTF 2022')
    b = bytes_to_long(b'IS_THIS_LCG?')
    x = getRandomInteger(1024)
    for i in range(8):
        x = (a * x + b) % m
        print('x{} = {}'.format(i, hex(x >> 850)))
    x = (a * x + b) % m
    return next_prime(x)
