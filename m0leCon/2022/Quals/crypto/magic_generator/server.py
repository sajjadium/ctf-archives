import random
import os

assert "FLAG" in os.environ
flag = os.environ["FLAG"]


def xor(arr):
    res = 0
    for a in arr:
        res ^= a
    return res


class MyGenerator:
    def __init__(self, nbits, l):
        self.l = l
        self.t = [0, 1, 2, 3, 9, 14]
        self.u = [random.randint(0, 1) for _ in range(nbits)]
        self.y = random.randrange(0, 2**nbits)
        self.z = 2*random.randrange(0, 2**(nbits-1))+1
        self.w = [(self.y * self.z**(nbits-i)) % (2**nbits) for i in range(nbits)]
        self.n = nbits

    def step(self):
        res = sum(uu*ww for uu, ww in zip(self.u, self.w)) % 2**(self.n)
        bit = xor([self.u[i] for i in self.t])
        self.u = self.u[1:]+[bit]
        return res >> self.l


def banner():
    print("Welcome to my newest magic trick!")
    print("I will give you some numbers, and you will have to guess the next ones")
    print("Let's begin!")
    print()


def main():
    banner()

    nbits = 128
    l = 40
    gen = MyGenerator(nbits, l)
    for _ in range(500):
        print(gen.step())

    print("Now it's your turn! Give me some numbers:")
    for _ in range(10):
        val = int(input())
        assert val == gen.step()

    print("Well done, you are a magician as well!")
    print("Here's something for you:", flag)


main()
