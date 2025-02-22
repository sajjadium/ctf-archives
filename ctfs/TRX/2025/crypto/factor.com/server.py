import random
from Crypto.Util.number import getPrime, bytes_to_long
flag = open('flag.txt', 'rb').read().strip()


def encrypt_flag():
    N = 1
    while N.bit_length() < 2048:
        N *= getPrime(random.randint(1,512))
    e = getPrime(random.randint(1024,2048))
    c = pow(bytes_to_long(flag), e, N)
    return N, e, c

try:
    while 1:
        N, e, c = encrypt_flag()
        print(f'N = {N}')
        print(f'e = {e}')
        print(f'c = {c}')
        new = input('Do you want to see another encryption? (yes/no): ')
        if new != 'yes':
            break
except Exception:
    pass
