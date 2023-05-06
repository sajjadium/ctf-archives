import random
import numpy as np

DIM = 256
q = 15901

rng = np.random.default_rng()

def gen_A():
    mat = [[random.randint(0, q-1) for _ in range(DIM)] for _ in range(DIM) ]
    return np.matrix(mat)


def gen_error_vec():
    e = [ rng.binomial(20, 0.5) - 10 for _ in range(DIM) ]
    return np.matrix(e).transpose()

def gen_error_mat():
    E = [ [rng.binomial(20, 0.5) - 10 for _ in range(DIM)] for _ in range(DIM) ]
    return np.matrix(E)


A = gen_A()
s = gen_error_vec()
# randomness is hard to come by, so we can save some by just reversing our secret
e = np.matrix(s.tolist()[::-1])
B = (A*s + e) % q

# Here's the public key!
print(f'A = {A.tolist()}')
print(f'B = {B.tolist()}')


flag = open('flag.txt', 'rb').read()
flag_hex = flag.hex()

flag_hex1 = flag_hex[0:DIM]
flag_hex1 += '0'*(DIM - len(flag_hex1))

# Four bits per entry
v1 = [ [(q // 2**4) * int(c, 16)] for c in flag_hex1 ] 
v1 = np.matrix(v1)

# Encrypt flag
def encrypt(msg):
    S_prime = gen_error_mat()
    E_prime = gen_error_mat()
    e_prime = gen_error_vec()

    B_prime = (S_prime * A + E_prime) % q
    V = (S_prime * B + e_prime + msg) % q

    return (B_prime, V)

ct = encrypt(v1)
print(f'B_prime = {ct[0].tolist()}')
print(f'V = {ct[1].tolist()}')

