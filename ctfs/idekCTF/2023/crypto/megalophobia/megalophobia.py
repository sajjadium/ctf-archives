#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, inverse
import os

# Local imports
with open('flag.txt', 'rb') as f:
    FLAG = f.read()
    f.close()

# Header
HDR = r"""|
|
|    ____    ____ ________   ______       _      _____      ___   _______ ____  ____   ___   ______  _____      _
|   |_   \  /   _|_   __  |.' ___  |     / \    |_   _|   .'   `.|_   __ \_   ||   _|.'   `.|_   _ \|_   _|    / \
|     |   \/   |   | |_ \_/ .'   \_|    / _ \     | |    /  .-.  \ | |__) || |__| | /  .-.  \ | |_) | | |     / _ \
|     | |\  /| |   |  _| _| |   ____   / ___ \    | |   _| |   | | |  ___/ |  __  | | |   | | |  __'. | |    / ___ \
|    _| |_\/_| |_ _| |__/ \ `.___]  |_/ /   \ \_ _| |__/ \  `-'  /_| |_   _| |  | |_\  `-'  /_| |__) || |_ _/ /   \ \_
|   |_____||_____|________|`._____.'|____| |____|________|`.___.'|_____| |____||____|`.___.'|_______/_____|____| |____|
|
|"""

# Private RSA key
d = 1
while d == 1:
    p, q = [getPrime(512) for _ in '01']
    d = inverse(0x10001, (p - 1)*(q - 1))

# Key encoding
num_byt = [i.to_bytes(256, 'big').lstrip(b'\x00') for i in [p, q, d, inverse(q, p)]]
sec_key = b''.join([len(k).to_bytes(2, 'big') + k for k in num_byt])

# OTP key to encrypt private part
otp_key = os.urandom((len(sec_key) - len(FLAG)) // 2) + b"__" + FLAG + b"__" + os.urandom(-((len(FLAG) - len(sec_key)) // 2))

pub_key = (p * q).to_bytes(128,'big')
enc_key = bytes([i^j for i,j in zip(sec_key, otp_key)])

# Server connection
print(HDR)

print("|  ~ Here hold my RSA key pair for me, don't worry, I encrypted the private part ::")
print('|    ' + pub_key.hex() + '::' + enc_key.hex())

print("|\n|  --- several hours later ---")
print('|\n|  ~ Hey, could you send me my encrypted private key?')

# Retrieve private key
try:
    my_enc_key = bytes.fromhex(input('|\n|    > (hex)'))
    my_sec_key = bytes([i^j for i,j in zip(my_enc_key, otp_key)])

    pop_lst = []
    while len(my_sec_key) >= 2:
        pop_len = int.from_bytes(my_sec_key[:2], 'big')
        if pop_len <= len(my_sec_key[2:]):
            pop_lst += [int.from_bytes(my_sec_key[2:2 + pop_len], 'big')]
            my_sec_key = my_sec_key[2 + pop_len:]
        else:
            my_sec_key = b""
    assert len(pop_lst) == 4

    p, q, d, u = pop_lst
    assert p * q == int.from_bytes(pub_key, 'big')

except:
    print("|\n|  ~ Erhm... That's not my key? I'll go somewhere else for now, bye...\n|")
    exit()

# RSA-CRT decryption function
def decrypt(cip, p, q, d, u):
    dp = d % (p - 1)
    dq = d % (q - 1)
    mp = pow(int.from_bytes(cip, 'big'), dp, p)
    mq = pow(int.from_bytes(cip, 'big'), dq, q)
    t = (mp - mq) % p
    h = (t * u) % p
    m = (h * q + mq)
    return m.to_bytes(128, 'big').lstrip(b'\x00')

# Game
print("|  ~ Now, I don't trust my own PRNG. Could you send me some 128-byte nonces encrypted with my RSA public key?")
for _ in range(500):

    enc_rng = bytes.fromhex(input('|  > '))

    nonce = decrypt(enc_rng, p, q, d, u)

    if len(nonce) < 128:
        print("|  ~ Erhm... are you sure this is a random 128-byte nonce? This doesn't seem safe to me... Q_Q")
    else:
        print("|  ~ Thanks, this looks random ^w^")