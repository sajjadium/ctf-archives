#!/usr/bin/env python3.8

from gmpy import next_prime
from random import getrandbits


def bytes_to_long(data):
    return int.from_bytes(data, 'big')


class Wardrobe:
    @staticmethod
    def create_boggarts(fear, danger):
        # for each level of danger we're increasing fear
        while danger > 0:
            fear = next_prime(fear)

            if getrandbits(1):
                yield fear
                danger -= 1


class Wizard:
    def __init__(self, magic, year, experience):
        self.magic = magic
        self.knowledge = year - 1 # the wizard is currently studying the current year
        self.experience = experience

    def cast_riddikulus(self, boggart):
        # increasing the wizard's experience by casting the riddikulus charm
        knowledge, experience = self.knowledge, self.experience

        while boggart > 1:
            knowledge, experience = experience, (experience * self.experience - knowledge) % self.magic
            boggart -= 1

        self.experience = experience


def main():
    year = 3
    bits = 512
    boggart_fear = 31337
    boggart_danger = 16

    neutral_magic, light_magic, dark_magic = [getrandbits(bits) for _ in range(3)]
    magic = next_prime(neutral_magic | light_magic) * next_prime(neutral_magic | dark_magic)

    print('Hello. I am Professor Remus Lupin. Today I\'m going to show you how to deal with the boggart.')

    print(neutral_magic)
    print(magic)

    with open('flag.txt', 'rb') as file:
        flag = file.read().strip()

    # some young wizards without knowledge of the riddikulus charm
    harry_potter = Wizard(magic, year, bytes_to_long(b'the boy who lived'))
    you = Wizard(magic, year, bytes_to_long(flag))

    for boggart in Wardrobe.create_boggarts(boggart_fear, boggart_danger):
        # wizards should train to learn the riddikulus charm
        harry_potter.cast_riddikulus(boggart)
        you.cast_riddikulus(boggart)

    # wizard's experience should be increased
    print(harry_potter.experience)
    print(you.experience)


if __name__ == '__main__':
    main()
