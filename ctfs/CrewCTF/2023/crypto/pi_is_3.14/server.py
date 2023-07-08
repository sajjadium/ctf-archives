import os
import signal

from flag import FLAG

N = 10000
M = 100


class XorShiftPlus:
    A = 10
    B = 15
    C = 7
    L = 23

    def __init__(self) -> None:
        self.x = int(os.urandom(4).hex(), 16)
        self.y = int(os.urandom(4).hex(), 16)

    def gen32(self) -> int:
        t = self.x
        s = self.y
        self.x = s
        t ^= (t << self.A) & 0xFFFFFFFF
        t ^= t >> self.B
        t ^= s ^ (s >> self.C)
        self.y = t
        return (s + t) & 0xFFFFFFFF

    def random(self) -> float:
        n32 = self.gen32()
        nL = 0
        # only L bits are used for 32-bit floating point
        for _ in range(self.L):
            nL *= 2
            nL += n32 & 1
            n32 >>= 1
        return nL / 2**self.L


def simulate(rand: XorShiftPlus) -> bool:
    a = rand.random()
    b = rand.random()
    r2 = a**2 + b**2
    return r2 < 1


if __name__ == "__main__":
    """
    Area of a quarter circle of radius 1 is pi/4
    Let's estimate pi by Monte Carlo simulation!
    """
    rand = XorShiftPlus()
    result = ""
    for _ in range(N):
        if simulate(rand):
            result += "o"
        else:
            result += "x"
    count = result.count("o")
    pi = count / N * 4
    print(result)
    print(f"\npi is {pi}")
    print(f"BTW, can you predict the following {M} simulation results?")
    signal.alarm(30)
    predicts = input("> ")
    assert len(predicts) == M
    assert len(set(predicts) - set("ox")) == 0
    for i in range(M):
        if simulate(rand):
            assert predicts[i] == "o"
        else:
            assert predicts[i] == "x"
    print(FLAG)
