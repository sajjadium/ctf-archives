import random
import math


class FCSR():
    def __init__(self, q: int, m: int, a: int):
        self.m = m
        self.q = q + 1
        self.k = int(math.log(q, 2))
        self.a = a

    @staticmethod
    def get_i(n: int, i: int) -> int:
        # right to left
        return (n & (0b1 << i)) >> i

    def clock(self) -> int:
        s = self.m
        for i in range(1, self.k + 1):
            s += self.get_i(self.q, i) * self.get_i(self.a, self.k - i)
        a_k = s % 2
        a_0 = self.a & 0b1
        self.m = s // 2
        self.a = (self.a >> 1) | (a_k << (self.k - 1))

        return a_0

    def encrypt(self, data: bytes) -> bytes:
        encrypted = b''
        for byte in data:
            key_byte = 0
            for _ in range(8):
                bit = self.clock()
                key_byte = (key_byte << 1) | bit
            encrypted += int.to_bytes(key_byte ^ byte, 1, 'big')

        return encrypted


if __name__ == '__main__':
    q = 509
    k = int(math.log(q + 1, 2))
    random.seed()
    a = random.randint(1, 2 ** k - 1)
    test = FCSR(q, 0, a)