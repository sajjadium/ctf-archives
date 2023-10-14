from Crypto.Util.number import bytes_to_long, isPrime
from functools import reduce
from secret import FLAG, SEED

class LFSR:
    def __init__(self, seed: int) -> None:
        assert 0 <= seed < 2**32, "Please provide a 32-bit seed."
        self.__state = list(map(int, "{:032b}".format(seed)))
        self.__taps = [31, 21, 1, 0]

    def __sum(self, v: list[int]) -> int:
        return reduce(lambda x, y: x^y, v, 0)

    def __tap(self) -> int:
        self.__state = [self.__sum([self.__state[idx] for idx in self.__taps])] + self.__state
        ret = self.__state.pop()
        return ret
    
    def getrandbits(self, n: int) -> int:
        ret = 0
        for _ in range(n):
            ret <<= 1
            ret += self.__tap()
        return ret

    def getrandprime(self, n: int) -> int:
        while True:
            ret = self.getrandbits(n)
            if isPrime(ret):
                return ret

def chall() -> None:
    e = 65537
    lfsr = LFSR(SEED)
    p = lfsr.getrandprime(1024)
    q = lfsr.getrandprime(1024)
    n = p * q
    m = bytes_to_long(FLAG)
    c = pow(m, e, n)

    with open("output.txt", "w") as f:
        f.write(f"{n = }\n{e = }\n{c = }")
    
chall()