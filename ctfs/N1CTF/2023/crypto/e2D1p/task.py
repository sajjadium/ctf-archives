from Crypto.Util.number import *
import os
FLAG = os.environ.get('FLAG', b'n1ctf{XXXXFAKE_FLAGXXXX}')
assert FLAG[:6] == b'n1ctf{' and FLAG[-1:] == b'}'
FLAG = FLAG[6:-1]


def keygen(nbits):
    while True:
        q = getPrime(nbits)
        if isPrime(2*q+1):
            if pow(0x10001, q, 2*q+1) == 1:
                return 2*q+1

def encrypt(key, message, mask):
    return pow(0x10001, message^mask, key)


p = keygen(512)
flag = bytes_to_long(FLAG)
messages = [getRandomNBitInteger(flag.bit_length()) for i in range(200)]
enc = [encrypt(p, message, flag) for message in messages]

print(f'message = {messages}')
print(f'enc = {enc}')