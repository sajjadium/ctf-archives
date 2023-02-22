class GF:
    def __init__(self, value):
        if type(value) == int:
            self.value = [(value // (3 ** i)) % 3 for i in range(5)]
        elif type(value) == list and len(value) == 5:
            self.value = value
        else:
            assert False, "Wrong input to the constructor"

    def __str__(self):
        return f"GF({self.to_int()})"

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(tuple(self.value))

    def __eq__(self, other):
        assert type(other) == GF
        return self.value == other.value
    
    def __add__(self, other):
        assert type(other) == GF
        return GF([(x + y) % 3 for x, y in zip(self.value, other.value)])
    
    def __sub__(self, other):
        assert type(other) == GF
        return GF([(x - y) % 3 for x, y in zip(self.value, other.value)])
    
    def __mul__(self, other):
        assert type(other) == GF

        arr = [0 for _ in range(9)]
        for i in range(5):
            for j in range(5):
                arr[i + j] = (arr[i + j] + self.value[i] * other.value[j]) % 3
        
        # Modulus: x^5 + 2*x + 1
        for i in range(8, 4, -1):
            arr[i - 4] = (arr[i - 4] - 2 * arr[i]) % 3
            arr[i - 5] = (arr[i - 5] - arr[i]) % 3
        
        return GF(arr[:5])
    
    def __pow__(self, other):
        assert type(other) == int
        base, ret = self, GF(1)
        while other > 0:
            if other & 1:
                ret = ret * base
            other >>= 1
            base = base * base
        return ret

    def inverse(self):
        return self ** 241

    def __div__(self, other):
        assert type(other) == GF
        return self * other.inverse()
    
    def to_int(self):
        return sum([self.value[i] * (3 ** i) for i in range(5)])

if __name__ == "__main__":
    assert GF(3) * GF(3) == GF(9)
    assert GF(9) * GF(27) == GF(5)
    assert GF(5).inverse() == GF(240)