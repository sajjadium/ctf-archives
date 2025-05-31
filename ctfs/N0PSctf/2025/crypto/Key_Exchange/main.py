from Crypto.Util import number
from random import randint
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import sys

N = 1024

def gen_pub_key(size):
    q = number.getPrime(size)
    k = 1
    p = k*q + 1
    while not number.isPrime(p):
        k += 1
        p = k*q + 1
    h = randint(2, p-1)
    g = pow(h, (p-1)//q, p)
    while g == 1:
        h = randint(2, p-1)
        g = pow(h, (p-1)//q, p)
    return p, g

def get_encrypted_flag(k):
    k = sha256(k).digest()
    iv = get_random_bytes(AES.block_size)
    data = open("flag", "rb").read()
    cipher = AES.new(k, AES.MODE_CBC, iv)
    padded_data = pad(data, AES.block_size)
    encrypted_data = iv + cipher.encrypt(padded_data)
    return encrypted_data

if __name__ == '__main__':
    p, g = gen_pub_key(N)
    a = randint(2, p-1)
    k_a = pow(g, a, p)
    sys.stdout.buffer.write(p.to_bytes(N))
    sys.stdout.buffer.write(g.to_bytes(N))
    sys.stdout.buffer.write(k_a.to_bytes(N))
    sys.stdout.flush()
    k_b = int.from_bytes(sys.stdin.buffer.read(N))
    k = pow(k_b, a, p)
    sys.stdout.buffer.write(get_encrypted_flag(k.to_bytes((k.bit_length() + 7) // 8)))
