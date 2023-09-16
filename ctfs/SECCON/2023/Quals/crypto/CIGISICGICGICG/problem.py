import os
from functools import reduce
from secrets import randbelow


flag = os.getenvb(b"FLAG", b"FAKEFLAG{THIS_IS_FAKE}")
p1 = 21267647932558653966460912964485513283
a1 = 6701852062049119913950006634400761786
b1 = 19775891958934432784881327048059215186
p2 = 21267647932558653966460912964485513289
a2 = 10720524649888207044145162345477779939
b2 = 19322437691046737175347391539401674191
p3 = 21267647932558653966460912964485513327
a3 = 8837701396379888544152794707609074012
b3 = 10502852884703606118029748810384117800


def prod(x: list[int]) -> int:
    return reduce(lambda a, b: a * b, x, 1)


def xor(x: bytes, y: bytes) -> bytes:
    return bytes([xi ^ yi for xi, yi in zip(x, y)])


class ICG:
    def __init__(self, p: int, a: int, b: int) -> None:
        self.p = p
        self.a = a
        self.b = b
        self.x = randbelow(self.p)

    def _next(self) -> int:
        if self.x == 0:
            self.x = self.b
            return self.x
        else:
            self.x = (self.a * pow(self.x, -1, self.p) + self.b) % self.p
            return self.x


class CIG:
    L = 256

    def __init__(self, icgs: list[ICG]) -> None:
        self.icgs = icgs
        self.T = prod([icg.p for icg in self.icgs])
        self.Ts = [self.T // icg.p for icg in self.icgs]

    def _next(self) -> int:
        ret = 0
        for icg, t in zip(self.icgs, self.Ts):
            ret += icg._next() * t
            ret %= self.T
        return ret % 2**self.L

    def randbytes(self, n: int) -> bytes:
        ret = b""
        block_size = self.L // 8
        while n > 0:
            ret += self._next().to_bytes(block_size, "big")[: min(n, block_size)]
            n -= block_size
        return ret


if __name__ == "__main__":
    random = CIG([ICG(p1, a1, b1), ICG(p2, a2, b2), ICG(p3, a3, b3)])
    enc_flag = xor(flag, random.randbytes(len(flag)))
    leaked = random.randbytes(300)
    print(f"{enc_flag = }")
    print(f"{leaked = }")
