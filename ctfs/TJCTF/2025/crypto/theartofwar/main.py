from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
import time


flag = open('flag.txt', 'rb').read()
m = bytes_to_long(flag)

e = getPrime(8)
print(f'e = {e}')

def generate_key():
    p, q = getPrime(256), getPrime(256)
    while (p - 1) % e == 0:
        p = getPrime(256)
    while (q - 1) % e == 0:
        q = getPrime(256)
    return p * q
    
for i in range(e):
    n = generate_key()
    c = pow(m, e, n)
    print(f'n{i} = {n}')
    print(f'c{i} = {c}')