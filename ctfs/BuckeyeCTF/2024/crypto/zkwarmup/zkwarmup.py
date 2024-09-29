from math import gcd
import random
import time
from flag import flag


class Verifier:
    def __init__(self, y, n):
        self.y = y
        self.n = n
        self.previous_ss = set()
        self.previous_zs = set()

    def flip_coin(self) -> int:
        return random.randrange(2)

    def verify(self, s, z, b) -> bool:
        if s in self.previous_ss or z in self.previous_zs:
            print("Bad: repeated s or z")
            return False

        self.previous_ss.add(s)
        self.previous_zs.add(z)

        n = self.n
        y = self.y
        if s == 0:
            print("Bad: s = 0")
            return False
        if gcd(s, n) != 1:
            print("Bad: gcd(s, n) != 1")
            return False
        return pow(z, 2, n) == (s * pow(y, 1 - b)) % n


def main():
    print("Welcome to zkwarmup!")

    # p = getPrime(1024)
    # q = getPrime(1024)
    # n = p * q
    n = 19261756194530262169516227535327268535825703622469356233861243450409596218324982327819027354327762272541787979307084854543427241827543331732057807638293377995167826046761991463655794445629511818504788588146049602678202660790161211079215140614149179394809442098536009911202757117559092796991732111808588753074002377241720729762405118846289128192452140379045358673985940236403266552967867241351260376075804662700969038717732248036975281084947926661161892037413944872628410488986135370175176475239647256670545733839891394321932103696968961386864456665963903759123610214930997530883831800104920546270573046968308379346633
    print(f"n = {n}")

    random.seed(int(time.time()))
    x = random.randrange(1, n)
    y = pow(x, 2, n)
    print(f"y = {y}")

    print("Can you prove that you know sqrt(y) without revealing it to the verifier?")
    verifier = Verifier(y, n)
    n_rounds = 128
    for i in range(n_rounds):
        s = int(input("Provide s: ")) % n
        b = verifier.flip_coin()
        print(f"b = {b}")

        z = int(input("Provide z: ")) % n
        if verifier.verify(s, z, b):
            print(f"Verification passed! {n_rounds - i - 1} rounds remaining")
        else:
            print("Verification failed!")
            return

    print("You've convinced the verifier you know sqrt(y)!")
    print(flag)


if __name__ == "__main__":
    main()
