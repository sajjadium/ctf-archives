#!/usr/bin/env python
from flag import FLAG
import time

class Spooder:
    def __init__(self):
         self.rand, self.i = int(time.time()), 2
         self.generate_random()

    def generate_random(self, m: int = 0x10ffff) -> int:
        self.rand = pow(self.i, self.rand, m)
        self.i = self.i + 1
        return self.rand

    def generate_padding(self, l: int = 0x101) -> str:
        padding = ''
        for i in range(self.generate_random(l)):
            padding += chr(self.generate_random(0xd7fb))
        return padding

spooder = Spooder()

def spooder_encryption(message: str) -> str:
    pad = spooder.generate_padding()
    message = ''.join([chr(ord(c) ^ spooder.generate_random(0xd7fb)) for c in message])
    cipher = pad + message
    return cipher

if __name__ == '__main__':

    welcome = f'''
               ▗▄▖ ▗▄▄▖ ▗▄ ▗▖  ▄▄
              ▗▛▀▜ ▐▛▀▜▌▐█ ▐▌ █▀▀▌
              ▐▙   ▐▌ ▐▌▐▛▌▐▌▐▌
               ▜█▙ ▐███ ▐▌█▐▌▐▌▗▄▖
                 ▜▌▐▌▝█▖▐▌▐▟▌▐▌▝▜▌
              ▐▄▄▟▘▐▌ ▐▌▐▌ █▌ █▄▟▌
               ▀▀▘ ▝▘ ▝▀▝▘ ▀▘  ▀▀
    \n
    This is not the RNG the world wants, and it's not the RNG the world need, but this is the RNG that the world gets.
    Welcome to the Spooder Random Number Generator, or special random number generator.
    It can generate random numbers like this: {', '.join([str(spooder.generate_random()) for _ in range(spooder.generate_random(121))])}.
    It can also generate random strings like this: {spooder.generate_padding(53)}.
    You can also use it to encrypt secrets like this: {spooder_encryption(FLAG).encode().hex()}.
    Here is a free trial:
    1. Generate random string.
    2. Generate random number.
    3. Encrypt.
    '''

    print(welcome)
    tries = spooder.generate_random(7)
    print(f'You have {tries} tries .')
    for _ in reversed(range(tries)):
        choice = input('Choose wisely:\n\t> ')
        if choice == '1':
            print(spooder.generate_padding(11))
        elif choice == '2':
            print(spooder.generate_random(101))
        elif choice == '3':
            print(spooder_encryption(input('what do you want to encrypt?\n\t> ')))
        else:
            exit(0)