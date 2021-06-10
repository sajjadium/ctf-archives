from math import sqrt
from itertools import count, islice

def sequence(index):
    """
    Generate a W*****l number given the index
    """
    element = (index << index) - 1
    return element

def is_prime(n):
    """
    Check if a given number is prime
    """
    return all(n % i for i in islice(count(2), int(sqrt(n)-1)))


key = [0x6b, 0x60, 0x72, 0x78, 0x30, 0x3d, 0x3f, 0x27, 0x5a, 0x4b, 0x24, 0x61, 0x7b, 0x3, 0x26, 0x68, 0x56, 
       0x73, 0x23, 0x49, 0x25, 0x35, 0x34, 0x77, 0x77, 0x22, 0x18, 0x34, 0x77, 0x5a, 0x6b, 0x60, 0x4d]

i = 2
while key != []:
    if is_prime(sequence(i)):
        print(chr(key[0]^i%100))
        key.pop(0)
        i += 1
    else:
        i += 1
