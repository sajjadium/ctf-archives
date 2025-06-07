#!/usr/local/bin/python3.10 -u

import time, sys, select
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class RandomGenerator:
    def __init__(self, seed = None, modulus = 2 ** 32, multiplier = 157, increment = 1):
        if seed is None: 
            seed = time.asctime()
        if type(seed) is int: 
            self.seed = seed
        if type(seed) is str: 
            self.seed = int.from_bytes(seed.encode(), "big")
        if type(seed) is bytes: 
            self.seed = int.from_bytes(seed, "big")
        self.m = modulus
        self.a = multiplier
        self.c = increment

    def randint(self, bits: int):
        self.seed = (self.a * self.seed + self.c) % self.m
        result = self.seed.to_bytes(4, "big")
        while len(result) < bits // 8:
            self.seed = (self.a * self.seed + self.c) % self.m
            result += self.seed.to_bytes(4, "big")
        return int.from_bytes(result, "big") % (2 ** bits)

    def randbytes(self, len: int):
        return self.randint(len * 8).to_bytes(len, "big")

def input_with_timeout(prompt, timeout=10):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.buffer.readline().rstrip(b'\n')
    raise Exception

def main():
    print("Welcome to the AES Oracle")
    
    randgen = RandomGenerator()
    cipher = AES.new(randgen.randbytes(32), AES.MODE_ECB)
    flag = open("flag.txt", "rb").read()

    ciphertext = cipher.encrypt(pad(flag, AES.block_size))
    print(f'{ciphertext = }')

    while True:
        plaintext = input_with_timeout("What would you like to encrypt? (enter 'quit' to exit) ")
        if plaintext == b"quit": break
        cipher = AES.new(randgen.randbytes(32), AES.MODE_ECB)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        print(f"{ciphertext = }")



if __name__ == "__main__":
    main()