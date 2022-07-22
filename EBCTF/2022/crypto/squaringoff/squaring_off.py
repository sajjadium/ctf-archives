#!/usr/bin/python

from Crypto.Util.number import bytes_to_long
from secret import flag

# parameters
BASE = 2
MODULUS = 0xfffffffe00000002fffffffe0000000100000001fffffffe00000001fffffffe00000001fffffffefffffffffffffffffffffffe000000000000000000000001

print( pow(BASE, bytes_to_long(flag), MODULUS) )
