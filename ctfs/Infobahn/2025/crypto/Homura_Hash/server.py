from os import getenv
from secrets import randbits

class Homura_Hash:
    def __init__(self, n, key):
        self.n = n
        self.key = []
        for shift, offset_0, offset_1, bit_select in key:
            assert 1 <= shift < n
            assert all(0 <= x < 2**n for x in [offset_0, offset_1, bit_select])
            self.key.append([shift, offset_0, offset_1, [bit for bit in range(n) if bit_select >> bit & 1]])
    def digest(self, text: int):
        assert 0 <= text < 2**self.n
        enc = 0
        for shift, offset_0, offset_1, bit_select in self.key:
            x = (text ^ offset_0) & (text ^ offset_1) >> shift
            for bit in bit_select:
                enc = enc << 1 | x >> bit & 1
        return enc

if __name__ == "__main__":
    flag = getenv("FLAG", "infobahn{fake_flag}")

    with open("key.txt") as file:
        n, m = map(int, file.readline().strip().split(" "))
        key = []
        for line in file.read().split("\n"):
            key.append(list(map(int, line.split(" "))))
    HH = Homura_Hash(n, key)
    secret_matrix = [randbits(m) for _ in range(n)]
    goal = randbits(m)

    print(goal)
    query = list(map(int, input("QUERY> ").split(" ")))
    assert 1 <= len(query) <= 600

    def transform(x):
        assert 0 <= x < 2**n and HH.digest(x) == 0
        y = 0
        for bit in range(n):
            if x >> bit & 1:
                y ^= secret_matrix[bit]
        return y
    print(" ".join(str(transform(x)) for x in query))
    if transform(int(input("ANSWER> "))) == goal:
        print(flag)
