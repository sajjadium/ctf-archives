#!/usr/bin/env python3.8

from os import urandom
from gmpy2 import next_prime
from random import randrange, getrandbits
from Crypto.Cipher import AES
from fastecdsa.curve import Curve


def bytes_to_long(data):
    return int.from_bytes(data, 'big')


def generate_random_point(p):
    while True:
        a, x, y = (randrange(0, p) for _ in range(3))
        b = (pow(y, 2, p) - pow(x, 3, p) - a * x) % p

        if (4 * pow(a, 3, p) + 27 * pow(b, 2, p)) % p != 0:
            break

    return Curve(None, p, a, b, None, x, y).G


class DarkWizard:
    def __init__(self, age):
        self.power = int(next_prime(getrandbits(age)))
        self.magic = generate_random_point(self.power)
        self.soul = randrange(0, self.power)

    def create_horcrux(self, location, weakness):
        # committing a murder
        murder = self.cast_spell(b'AVADA KEDAVRA')

        # splitting the soul in half
        self.soul = self.soul * pow(2, -1, self.power) % self.power

        # making a horcrux
        horcrux = (self.soul + murder) * self.magic

        # nobody should know location and weakness of the horcrux
        horcrux.x ^= location
        horcrux.y ^= weakness

        return horcrux

    def cast_spell(self, spell_name):
        spell = bytes_to_long(spell_name)

        return spell %~ spell


def encrypt(key, plaintext):
    cipher = AES.new(key=key, mode=AES.MODE_ECB)
    padding = b'\x00' * (AES.block_size - len(plaintext) % AES.block_size)

    return cipher.encrypt(plaintext + padding)


def main():
    wizard_age = 3000
    horcruxes_count = 2

    wizard = DarkWizard(wizard_age)
    print(f'Wizard\'s power:\n{hex(wizard.power)}\n')
    print(f'Wizard\'s magic:\n{wizard.magic}\n')

    key = urandom(AES.key_size[0])
    horcrux_length = len(key) // horcruxes_count

    for i in range(horcruxes_count):
        key_part = key[i * horcrux_length:(i + 1) * horcrux_length]

        horcrux_location = bytes_to_long(key_part[:horcrux_length // 2])
        horcrux_weakness = bytes_to_long(key_part[horcrux_length // 2:])

        horcrux = wizard.create_horcrux(horcrux_location, horcrux_weakness)
        print(f'Horcrux #{i + 1}:\n{horcrux}\n')

    with open('flag.txt', 'rb') as file:
        flag = file.read().strip()

    ciphertext = encrypt(key, flag)
    print(f'Ciphertext:\n{ciphertext.hex()}')


if __name__ == '__main__':
    main()
