import os
from random import SystemRandom
from Crypto.Util.number import isPrime, long_to_bytes
from Crypto.Cipher import AES
from math import ceil


def pad(arr: bytes, size: int) -> bytes:
    arr += (16 * size - len(arr)) * b'\x00'
    return arr


class challenge:
    def __init__(self, bit_cnt: int, no_primes: int):
        self.bit_cnt = bit_cnt
        self.no_primes = no_primes
        self.aes_key = os.urandom(16)
        self.aes_iv = os.urandom(16)
        self.random = SystemRandom()
        self.block_cnt = int(ceil(self.bit_cnt * self.no_primes / 128))

    def _get_prime_number(self) -> int:
        prime_number = self.random.randrange(2 ** (self.bit_cnt - 1) + 1, 2 ** self.bit_cnt - 1)

        while not isPrime(prime_number):
            prime_number = self.random.randrange(2 ** (self.bit_cnt - 1) + 1, 2 ** self.bit_cnt - 1)

        return prime_number

    def _get_modulo(self) -> int:
        n = 1
        used_primes = {2}
        for i in range(self.no_primes):
            new_prime = self._get_prime_number()
            
            while new_prime in used_primes:
                new_prime = self._get_prime_number()
            
            used_primes.add(new_prime)
            n *= new_prime

        while not isPrime(2 * n + 1):
            n = 1
            used_primes = {2}
            for i in range(self.no_primes):
                new_prime = self._get_prime_number()
                
                while new_prime in used_primes:
                    new_prime = self._get_prime_number()
                
                used_primes.add(new_prime)
                n *= new_prime

        return 2 * n + 1

    def _get_random_secret_pair(self, n) -> (int, bytes):
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)
        k = self.random.randrange(0, n - 1)
        enc_k = aes_cipher.encrypt(pad(long_to_bytes(k), self.block_cnt))

        return k, enc_k

    def get_challenge(self) -> (int, int, bytes):
        print("Loading...\n")
        n = self._get_modulo()
        k, enc_k = self._get_random_secret_pair(n)
        return n, k, enc_k

    def encrypt(self, n: int, base: int, exponent: int) -> bytes:
        x = pow(base, exponent, n)
        aes_cipher = AES.new(self.aes_key, AES.MODE_CBC, self.aes_iv)

        return aes_cipher.encrypt(pad(long_to_bytes(x), self.block_cnt))
