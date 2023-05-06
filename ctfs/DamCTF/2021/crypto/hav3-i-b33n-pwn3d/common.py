#!/usr/bin/env sage

from sage.all import *
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint_number_field

from Crypto.Hash import MD5, SHA256
from Crypto.Random import random as crypt_random


curve25519_p = 2**255 - 19
F = GF(curve25519_p)
R = F['x']
x = R.gen()

curve25519 = EllipticCurve(F, [0, 486662, 0, 1, 0])
#assert(curve25519.count_points() == 57896044618658097711785492504343953926856930875039260848015607506283634007912)


# cofactor == bad?
def sample_R():
    return (crypt_random.randrange(2**255) >> 3) <<3

def md5(msg: bytes) -> int:
    h = MD5.new()
    h.update(msg)
    return int.from_bytes(h.digest(), 'little')

def sha(msg: bytes) -> bytes:
    h = SHA256.new()
    h.update(msg)
    return h.digest()



def xy_to_curve(x, y):
    return EllipticCurvePoint_number_field(curve25519, (x, y, 1), check=False)

base_p = xy_to_curve(9, 43114425171068552920764898935933967039370386198203806730763910166200978582548)
