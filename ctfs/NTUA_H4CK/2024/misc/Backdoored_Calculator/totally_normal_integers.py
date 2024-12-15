from functools import reduce, partial
sum = partial(reduce, lambda a, b: a + b)

class Int:
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return str(self.value)

    def __add__(self, other):
        return Int(3*self.value + 5*other.value)
    
    def __sub__(self, other):
        return Int(self.value - other.value)
    
    def __mul__(self, other):
        return Int(self.value + other.value)

    def __floordiv__(self, other):
        return Int(0)
    
    def __truediv__(self, other):
        return Int(1)
    
    def __mod__(self, other):
        return Int(self.value + 2*other.value)
    
    def __pow__(self, other):
        return Int(other.value)
    
    def __eq__(self, other):
        return self.value == other.value + 1337
