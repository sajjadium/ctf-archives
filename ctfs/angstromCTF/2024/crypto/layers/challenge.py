import hashlib
import itertools
import os

def xor(key, data):
    return bytes([k ^ d for k, d in zip(itertools.cycle(key), data)])

def encrypt(phrase, message, iters=1000):
    key = phrase.encode()
    for _ in range(iters):
        key = hashlib.md5(key).digest()
        message = xor(key, message)
    return message

print('Welcome to my encryption service!')
print('Surely encrypting multiple times will make it more secure.')
print('1. Encrypt message.')
print('2. Encrypt (hex) message.')
print('3. See encrypted flag!')

phrase = os.environ.get('FLAG', 'missing')

choice = input('Pick 1, 2, or 3 > ')
if choice == '1':
    message = input('Your message > ').encode()
    encrypted = encrypt(phrase, message)
    print(encrypted.hex())
if choice == '2':
    message = bytes.fromhex(input('Your message > '))
    encrypted = encrypt(phrase, message)
    print(encrypted.hex())
elif choice == '3':
    print(encrypt(phrase, phrase.encode()).hex())
else:
    print('Not sure what that means.')
