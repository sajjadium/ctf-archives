from sage.all import *
from Crypto.Util.number import bytes_to_long

class RNG:

    def __init__(self, seed):
        self.p = next_prime(2**24)
        self.F = GF(self.p)
        self.M = matrix(self.F, 3,3, [bytes_to_long(seed[i:i+3]) for i in range(0, len(seed), 3)])
        self.state = vector(self.F, map(ord, "Mvm"))
        self.gen = self.F(2)

    def get_random_num(self):
        out = self.M * self.state

        for i in range(len(self.state)):
            self.state[i] = self.gen**self.state[i]

        return out * self.state

flag = b"MVM{???????????????????????????}"
seed = flag[4:-1]

rng = RNG(seed)
samples = []

for i in range(9):
    samples.append(rng.get_random_num())

print(f"{samples = }")
# samples = [6192533, 82371, 86024, 4218430, 12259879, 16442850, 6736271, 7418630, 15483781]
