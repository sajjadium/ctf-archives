from secrets import randbits
from Crypto.Hash import SHAKE256
import re


Magic_Latin_Square = [[5, 3, 1, 6, 7, 2, 0, 4],
                      [3, 5, 0, 2, 4, 6, 1, 7],
                      [6, 2, 4, 5, 0, 3, 7, 1],
                      [4, 7, 6, 1, 3, 0, 2, 5],
                      [0, 1, 3, 7, 6, 4, 5, 2],
                      [7, 4, 2, 0, 5, 1, 6, 3],
                      [2, 6, 7, 3, 1, 5, 4, 0],
                      [1, 0, 5, 4, 2, 7, 3, 6]]


class Magic():
    def __init__(self, N):
        self.N = N

    def __call__(self, x):
        if isinstance(x, int):
            return MagicElement(x)
        elif isinstance(x, list):
            return MagicList(self, x)
        elif isinstance(x, str):
            return MagicList(self, [int(i) for i in x])

    def random_element(self):
        return randbits(3)

    def random_list(self, n):
        return (MagicList(self, [self.random_element() for _ in range(self.N)]) for i in range(n))

    def shake(self, something):
        H = SHAKE256.new()
        H.update(something)
        H = re.findall(r'\d{3}', bin(int.from_bytes(
            H.read(384 // 8), 'big'))[2:].zfill(3*self.N))
        return self([int(i, 2) for i in H])


class MagicElement():
    def __init__(self, value):
        self.value = int(value) % 8

    def __eq__(self, other):
        return self.value == other.value

    def __add__(self, other):
        return MagicElement(Magic_Latin_Square[self.value][other.value])

    def __str__(self):
        return str(self.value)


class MagicList():
    def __init__(self, magic, lst):
        self.magic = magic
        self.N = magic.N
        self.U = [_ for _ in self.generator(self.N**2+1)]
        if isinstance(lst, MagicList):
            self.lst = lst.lst
        elif isinstance(lst[0], int):
            self.lst = [MagicElement(_) for _ in lst]
        elif isinstance(lst[0], MagicElement):
            self.lst = [_ for _ in lst]

    def generator(self, x):
        U = [(7*(3*i+5)**17+11) % self.N for i in range(self.N)]
        for i in range(x):
            yield U[i % self.N]
            if self.N-i % self.N == 1:
                V = U[:]
                for j in range(self.N):
                    U[j] = V[U[j]]
            i = i + 1
        return

    def mix(self, T, K):
        R = T+K
        e = self.U[0]
        for i in range(self.N ** 2):
            d = self.U[i+1]
            R.lst[d] = R.lst[d] + R.lst[e]
            e = d
        R = R+K
        return R

    def __add__(self, other):
        R = []
        for i in range(self.N):
            R.append(self.lst[i] + other.lst[i])
        return MagicList(self.magic, R)

    def __mul__(self, other):
        return MagicList(self.magic, self.mix(self, other))

    def __eq__(self, other):
        for i in range(len(self.lst)):
            if self.lst[i].value != other.lst[i].value:
                return False
        return True

    def __str__(self):
        if isinstance(self.lst[0], int):
            return ''.join([str(i) for i in self.lst])
        elif isinstance(self.lst[0], MagicElement):
            return ''.join([str(i.value) for i in self.lst])

    def __len__(self):
        return len(self.lst)
