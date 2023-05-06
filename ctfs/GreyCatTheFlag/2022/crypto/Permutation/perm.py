class Perm():
    def __init__(self, arr):
        assert self.valid(arr)
        self.internal = arr
        self.n = len(arr)

    def valid(self, arr):
        x = sorted(arr)
        n = len(arr)
        for i in range(n):
            if (x[i] != i):
                return False
        return True

    def __str__(self):
        return ",".join(map(str, self.internal))

    def __mul__(self, other):
        assert other.n == self.n
        res = []
        for i in other.internal:
            res.append(self.internal[i])
        return Perm(res)

    def __pow__(self, a):
        res = Perm([i for i in range(self.n)])
        g = Perm(self.internal)
        while (a > 0):
            if (a & 1): res = res * g
            g = g * g
            a //= 2
        return res
