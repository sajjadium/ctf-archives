from Crypto.Util.number import getPrime
from secret import flag
import random

class RNG:
    def __init__(self, s, a):
        self.s = s
        self.a = a

    def next(self):
        self.s = (self.s * self.a) % (2 ** 128)
        return self.s >> 96


if __name__ == "__main__":
    rng1 = RNG(getPrime(128), getPrime(64))
    rng2 = RNG(getPrime(128), getPrime(64))

    assert flag.startswith("maple{") and flag.endswith("}")
    flag = flag[len("maple{"):-1]

    enc_flag = []
    for i in range(0, len(flag), 4):
        enc_flag.append(int.from_bytes(flag[i:i+4].encode(), 'big') ^ rng1.next() ^ rng2.next())
    
    outputs = []
    for _ in range(42):
        if random.choice([True, False]):
            rng1.next()
        
        if random.choice([True, False]):
            rng2.next()

        if random.choice([True, False]):
            outputs.append(rng1.next())
        else:
            outputs.append(rng2.next())


    print("RNG 1:", rng1.a)
    print("RNG 2:", rng2.a)
    print("Encrypted flag:", enc_flag)
    print("Outputs:", outputs)
