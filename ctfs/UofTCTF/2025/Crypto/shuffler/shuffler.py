#! /usr/local/bin/python3
from fractions import Fraction
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from hashlib import sha256

def Bake(x,y):
    if y <= 1 / 2:
        x, y = x / 2, 2 * y
    elif y >= 1 / 2:
        x, y = 1 - x / 2, 2 - 2 * y
    return x,y

class PRNG:
    def __init__(self, initial_state):
        self.x = initial_state[0]
        self.y = initial_state[1]

    def next(self):
        num = self.x + self.y
        self.x, self.y = Bake(self.x, self.y)
        return num

    def random_number(self, n=1):
        return int(self.next()*n/2)


class Arrangement:
    def __init__(self, seed, n):
        self.seed = seed
        self.nums = [i for i in range(1, n+1)]
        self.shuffle(n)

    def shuffle(self, n):
        new_nums = []
        for i in range(n):
            num_index = self.seed % (n - i)
            new_nums.append(self.nums.pop(num_index))
            self.seed //= (n - i)
        self.nums = new_nums


if __name__ == "__main__":
    flag = b'uoftctf{...}'
    initial_x = Fraction('...')
    initial_y = Fraction('...') 
    k = int('...')
    assert 0 <initial_y < 1 and 0 < initial_x < 1 and 0 < k < 100
    y_hint1 = initial_y * Fraction(f'{2**k - 1}/{2**k}') * (2 ** k)
    x_hint1 = initial_x * Fraction(f'{2**k - 1}/{2**k}') * (2 ** k)
    assert y_hint1.denominator == 1 and x_hint1.denominator == 1
    y_hint2 = int(bin(y_hint1.numerator)[:1:-1], 2)
    x_hint2 = int(bin(x_hint1.numerator)[2:], 2)
    assert x_hint2 == y_hint2 << 1
    rng = PRNG((initial_x, initial_y))
    key = sha256(long_to_bytes(rng.random_number(2**100))).digest()
    cipher = AES.new(key, AES.MODE_ECB)
    flag = cipher.encrypt(flag)
    print(f"Welcome to the shuffler! Here's the flag if you are here for it {flag.hex()}.")
    while True:
        bound = int(input("Give me an upper bound for a sequence of numbers, I'll shuffle it for you! "))
        if bound < 1:
            print("Pick positive numbers!")
            continue
        if bound > 30:
            print("That's too much for me!")
            continue
        print(Arrangement(rng.random_number(2**100), bound).nums)