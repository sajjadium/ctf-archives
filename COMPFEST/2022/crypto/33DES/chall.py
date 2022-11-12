from des_lib import *
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from flag import FLAG
import os

def lrot(s, n):
    for _ in range(n):
        s = s[1:] + s[0]
    return s

def generate_keys():
    key_bits = bin(b2l(KEY[0]))[2:].zfill(64)
    permuted_key = ''.join([key_bits[i] for i in PERMUTED_CHOICE_1])

    a = [permuted_key[:len(permuted_key) // 2]]
    b = [permuted_key[len(permuted_key) // 2:]]

    for i, rot in enumerate(BITS_ROT_TABLE):
        a.append(lrot(a[i], rot))
        b.append(lrot(b[i], rot))

    for i in range(1, 17):
        a_b = a[i] + b[i]
        key_bits = ''.join([a_b[j] for j in PERMUTED_CHOICE_2])
        KEY.append(int(key_bits, 2).to_bytes(6, 'big'))

def xor(a, b):
    return ''.join([str(int(i) ^ int(j)) for i, j in zip(a, b)])

def sumn(a):
    return int((1 << 4) - 0xf / 8 * (a - 1))

def S(bits, i):
    return '{0:04b}'.format(S_BOXES[i][int(bits[0] + bits[-1], 2)][int(bits[1:-1], 2)])

def F(bits, key):
    e = ''.join([bits[i] for i in EXPANSION_FUNCTION])
    key_bits = bin(b2l(key))[2:].zfill(48)

    xored = xor(key_bits, e)
    s = ''.join([S(xored[i:i+6], i//6) for i in range(0, len(xored), 6)])

    return ''.join([s[i] for i in P])

def encrypt(plain, n):
    plain_bits = bin(b2l(plain))[2:].zfill(64)
    permuted = ''.join([plain_bits[i] for i in INITIAL_PERMUTATION])

    l = [permuted[:len(permuted) // 2]]
    r = [permuted[len(permuted) // 2:]]
    for i in range(n):
        l.append(r[i])
        r.append(xor(l[i], F(r[i], KEY[i+1])))

    r_l = r[-1] + l[-1]
    permuted_final = ''.join([r_l[i] for i in FINAL_PERMUTATION])

    return int(permuted_final, 2).to_bytes(8, 'big')  

KEY = [os.urandom(8)]
generate_keys()

with open('flag.enc', 'w') as fout:
    for i in range(1,10):
        cipher = b''.join([encrypt(FLAG[j:j+8], sumn(i)) for j in range(0, len(FLAG), 8)])
        print(cipher.hex(), file=fout)
