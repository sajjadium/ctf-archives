import time
import os
import sys


class Random:
    def __init__(self, seed=None):
        if seed is None:
            self.seed = int(time.time() * (10 ** 7))
        else:
            try:
                self.seed = int(seed)
            except ValueError:
                raise ValueError("Please use a valid integer for the seed.")
        self.next_seed = 0

    def __generatePercentage(self):
        a = 1664525
        c = 1013904223
        m = 2 ** 32

        if self.next_seed == 0:
            next_seed = (self.seed * a + c) % m
        else:
            next_seed = (self.next_seed * a + c) % m
        self.next_seed = next_seed
        randomPercentage = next_seed / m

        return randomPercentage

    def choice(self, index):
        randomIndex = round((self.__generatePercentage() * (len(index) - 1)))
        randomChoice = index[randomIndex]

        return randomChoice


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python passwordgen.py <int>")
        exit(1)
    else:
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890?!@#$%^&*()"
        rand = Random(os.getpid())
        password = ''.join([rand.choice(alphabet) for i in range(int(sys.argv[1]))])
        print(password)