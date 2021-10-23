#!/usr/bin/env python3
import random
import os

rand = random.SystemRandom()
FLAG = b"buckeye{?????????????????????}"


def is_prime(n, rounds=32):
    return all(pow(rand.randrange(2, n), n - 1, n) == 1 for _ in range(rounds))


class RNG:
    def __init__(self, p: int, a: int):
        self.p = p
        self.a = a

    def next_bit(self) -> int:
        ans = pow(self.a, (self.p - 1) // 2, self.p)
        self.a += 1
        return int(ans == 1)

    def next_byte(self) -> int:
        ans = 0
        for i in range(8):
            ans |= self.next_bit() << i
        return ans

    def next_bytes(self, n: int) -> bytes:
        return bytes(self.next_byte() for _ in range(n))


def main():
    p = int(input("Give me a prime number: "))

    if not (256 <= p.bit_length() <= 512):
        print("Wrong bit length")
        return

    if not is_prime(p):
        print("Fermat tells me your number isn't prime")
        return

    a = rand.randrange(2, p)
    rng = RNG(p, a)

    plaintext = b"Hello " + os.urandom(48).hex().encode()
    print("Have some ciphertexts:")

    for _ in range(32):
        s = rng.next_bytes(len(plaintext))
        c = bytes(a ^ b for a, b in zip(s, plaintext))
        print(c.hex())

    if plaintext == input("Guess the plaintext:\n").encode():
        print(f"Congrats! Here's the flag: {FLAG}")
    else:
        print("That's wrong")


main()
