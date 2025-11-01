import os, secrets, signal

def hash(params, msg):
    a, b, c, m, x = params
    for byte in msg:
        for bit in f'{byte:08b}':
            x = ((x * a + b + int(bit)) ^ c) % m
    return x

nbits = 128
rand = lambda: secrets.randbits(nbits)
print('⚙️', params := (rand() | 1, rand(), rand(), 2 ** nbits, rand()))
print('🎯', target := rand())

signal.alarm(900)
message = bytes.fromhex(input('💬 '))
assert hash(params, message) == target, '❌'
print('🚩', os.getenv("FLAG"))
