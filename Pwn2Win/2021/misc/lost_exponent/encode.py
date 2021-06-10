from math import sqrt
from random import seed, shuffle
from lost import e, flag
from itertools import product
from numpy import sign, diff


assert flag.startswith('CTF-BR{')
seed(6174)
n = int(sqrt(len(flag))) + 2
order = list(product(range(n), repeat=2))
shuffle(order)
order.sort(key=(lambda x: sign(diff(x))))


class Matrix:
    def __init__(self):
        self.n = n
        self.m = [[0]*n for _ in range(n)]

    def __iter__(self):
        for i in range(self.n):
            for j in range(self.n):
                yield self.m[i][j]

    def I(self):
        r = Matrix()
        for i in range(n):
            r[i, i] = 1
        return r

    def __setitem__(self, key, value):
        self.m[key[0]][key[1]] = value

    def __getitem__(self, key):
        return self.m[key[0]][key[1]]

    def __mul__(self, other):
        r = Matrix()
        for i in range(n):
            for j in range(n):
                r[i, j] = sum(self[i, k]*other[k, j] for k in range(n))
        return r

    def __pow__(self, power):
        r = self.I()
        for _ in range(power):
            r = r * self
        return r

    def __str__(self):
        return str(self.m)


if __name__ == '__main__':
    m = Matrix()
    for i, f in zip(order, flag):
        m[i] = ord(f)
    cflag = list(map(str, m ** e))
    mn = max(map(len, cflag))
    mn += mn % 2
    cflag = ''.join(b.zfill(mn) for b in cflag)
    cflag = bytes([int(cflag[i:i+2]) for i in range(0, len(cflag), 2)])

    with open('enc', 'wb') as out:
        out.write(cflag)