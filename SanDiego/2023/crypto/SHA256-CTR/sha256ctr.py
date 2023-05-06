import hashlib
from random import SystemRandom
import secrets
from time import sleep

FLAG = open('flag.txt', 'rb').read()
# In bits
INITIAL_CTR_SIZE = 256

SHA256_SIZE = 32

counter = secrets.randbelow(2 ** INITIAL_CTR_SIZE)

# print(hex(counter)) # DEBUG

print('Welcome to the demo playground for my unbreakable SHA256-CTR encryption scheme')
print('It is inspired by AES-CTR + SHA256, none of which has been shown to be breakable')

def next_key_block():
    global counter
    cb = counter.to_bytes((counter.bit_length() + 7) // 8, 'little')
    counter += 1
    # print('cb:', cb.hex()) # DEBUG
    # print('key:', hashlib.sha256(cb).digest().hex()) # DEBUG
    return hashlib.sha256(cb).digest()

sleep_time_gen = SystemRandom()

def rate_limit():
    print('Thinking...')
    sleep((1 + sleep_time_gen.random()) / 4)

def xor(sa: bytes, sb: bytes):
    return bytes([a ^ b for a, b in zip(sa, sb)])

def encrypt(b: bytes) -> bytes:
    return b''.join(xor(b[i:i+SHA256_SIZE], next_key_block()) for i in range(0,len(b),SHA256_SIZE))

while True:
    print('Menu:')
    print('1. Encrypt the flag')
    print('2. Encrypt your own message')
    print('3. Simulate encrypting N blocks')
    print('4. Exit')
    try:
        choice = input('> ')
    except EOFError:
        print()
        break
    if choice == '1':
        rate_limit()
        print(f'Ciphertext in hex: {encrypt(FLAG).hex()}')
    elif choice == '2':
        hx = input('Enter your message in hex: ')
        try:
            msg = bytes.fromhex(hx)
        except ValueError:
            print('Invalid hex sequence')
            continue
        rate_limit()
        print(f'Ciphertext in hex: {encrypt(msg).hex()}')
    elif choice == '3':
        # Developer note:
        # Debug feature, should have zero impact on security
        # since you can just do those N-block encryptions yourself using option 1 and 2, right?
        try:
            i = int(input('N = '))
        except ValueError:
            print('You must enter a valid integer')
            continue
        if i >= 0:
            rate_limit()
            counter = counter + i
        else:
            print('N must be non-negative')
    elif choice == '4':
        print('Come back when you can break the unbreakable.')
        break
    else:
        print('Unknown option!')