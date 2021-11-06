#!/usr/bin/env sage

from sage.all import *
from sage.schemes.elliptic_curves.ell_point import EllipticCurvePoint_number_field

from Crypto.Cipher import AES

# The description of CrownRNG is too unclear, and the system random number
# generator is bound to be more secure anyway.
from Crypto.Random import random as crypt_random

curve25519_p = 2**255 - 19
F = GF(curve25519_p)

curve25519 = EllipticCurve(F, [0, 486662, 0, 1, 0])
assert(curve25519.count_points() == 57896044618658097711785492504343953926856930875039260848015607506283634007912)

def sample_R():
    # shift is to clear the cofactor
    return (crypt_random.randrange(2**255) >> 3) <<3

def shared_aes_key(point) -> bytes:
    return AES.new(int(point.xy()[0]).to_bytes(256 // 8, 'little'), AES.MODE_CTR)

def xy_to_curve(x, y):
    return EllipticCurvePoint_number_field(curve25519, (x, y, 1), check=False)

base_p = xy_to_curve(9, 43114425171068552920764898935933967039370386198203806730763910166200978582548)

### execute both parties and print the transcript.

## section 4.I.b

# alice
a = sample_R()
A = a*base_p
print(f'A: {A}')

# bob
b = sample_R()
B = b*base_p
print(f'B: {B}')

# alice
Ka = a*B

# bob
Kb = b*A

assert(Ka == Kb)

## section 4.I.c

# alice
aes = shared_aes_key(Ka)
last_digit_idx = crypt_random.randrange(4)
start_index = crypt_random.randrange(132, 193)
params = f'{last_digit_idx},{start_index:9}'.encode()
enc_params = aes.encrypt(params)
print(f'enc_params: {enc_params.hex()}')

with open("flag", 'r') as f:
    message = f"Psst! Bob, don't tell anyone, but the flag is {f.read().strip()}.".encode()

msg_bits = 8 * len(message)
NPSN = 10 * int(Ka.xy()[0]) + [2, 3, 7, 8][last_digit_idx]
key_stream = N(sqrt(NPSN), start_index + msg_bits).sign_mantissa_exponent()[1]
key_stream &= (2**msg_bits - 1)
key_stream = int(key_stream).to_bytes(len(message), 'big')

enc_msg = bytes([x ^ y for x, y in zip(message, key_stream)])
print(f'enc_msg: {enc_msg.hex()}')
