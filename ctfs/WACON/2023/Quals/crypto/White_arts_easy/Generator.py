import os
from RandomFunction import RandomFunction
from RandomPermutation import RandomPermutation

def xor(a : bytes, b : bytes):
    return bytes([u ^ v for u,v in zip(a,b)])

class Generator1:
    def __init__(self):
        self.mode = os.urandom(1)[0] & 1
        self.n = 8
        self.input_size = 2 * self.n
        self.RF_gen = RandomFunction(self.n)
        self.RF_random = RandomFunction(2 * self.n)
    
    def func_gen(self, q):
        L, R = q[:self.n], q[self.n:]
        L, R = R, xor(L, self.RF_gen.query(R))
        return L+R

    def func_random(self, q):
        return self.RF_random.query(q)

    def calc(self, q, inverse):
        assert inverse == False, "inverse query is not allowed for Generator1"
        ret_gen = self.func_gen(q)
        ret_random = self.func_random(q)
        if self.mode == 0:
            return ret_gen
        else:
            return ret_random

class Generator2:
    def __init__(self):
        self.mode = os.urandom(1)[0] & 1
        self.n = 8
        self.input_size = 2 * self.n
        self.RF_gen = RandomFunction(self.n)
        self.RF_random = RandomFunction(2 * self.n)
    
    def func_gen(self, q):
        L, R = q[:self.n], q[self.n:]
        L, R = R, xor(L, self.RF_gen.query(R))
        L, R = R, xor(L, self.RF_gen.query(R))
        return L+R

    def func_random(self, q):
        return self.RF_random.query(q)

    def calc(self, q, inverse):
        assert inverse == False, "inverse query is not allowed for Generator2"
        ret_gen = self.func_gen(q)
        ret_random = self.func_random(q)
        if self.mode == 0:
            return ret_gen
        else:
            return ret_random

class Generator3:
    def __init__(self):
        self.mode = os.urandom(1)[0] & 1
        self.n = 8
        self.input_size = 2 * self.n
        self.RF_gen = RandomFunction(self.n)
        self.RF_random = RandomPermutation(2 * self.n)
    
    def func_gen(self, q, inverse):
        if not inverse:
            L, R = q[:self.n], q[self.n:]
            L, R = R, xor(L, self.RF_gen.query(R))
            L, R = R, xor(L, self.RF_gen.query(R))
            L, R = R, xor(L, self.RF_gen.query(R))


        else:
            L, R = q[:self.n], q[self.n:]
            L, R = xor(R, self.RF_gen.query(L)), L
            L, R = xor(R, self.RF_gen.query(L)), L
            L, R = xor(R, self.RF_gen.query(L)), L

        return L+R

    def func_random(self, q, inverse):
        return self.RF_random.query(q, inverse)

    def calc(self, q, inverse):        
        ret_gen = self.func_gen(q, inverse)
        ret_random = self.func_random(q, inverse)
        if self.mode == 0:
            return ret_gen
        else:
            return ret_random

class Generator4:
    def __init__(self):
        self.mode = os.urandom(1)[0] & 1
        self.n = 8
        self.input_size = 2 * self.n
        self.RF_gen = RandomPermutation(self.n)
        self.RF_random = RandomPermutation(2 * self.n)
    
    def func_gen(self, q, inverse):
        X, T = q[:self.n], q[self.n:]
        X = xor(X, T)
        X = self.RF_gen.query(X, inverse)
        X = xor(X, T)
        X = self.RF_gen.query(X, inverse)
        X = xor(X, T)
                                   
        return X

    def func_random(self, q, inverse):
        return self.RF_random.query(q, inverse)[:self.n]

    def calc(self, q, inverse):        
        ret_gen = self.func_gen(q, inverse)
        ret_random = self.func_random(q, inverse)
        if self.mode == 0:
            return ret_gen
        else:
            return ret_random

class Generator5:
    def __init__(self):
        self.mode = os.urandom(1)[0] & 1
        self.n = 1
        self.input_size = self.n
        self.RF_gen = [RandomPermutation(self.n) for _ in range(4)]
        self.RF_random = RandomFunction(self.n)
    
    def func_gen(self, q):
        ret = bytes(1)
        for i in range(4):
            ret = xor(ret, self.RF_gen[i].query(q))
        return ret

    def func_random(self, q):
        return self.RF_random.query(q)

    def calc(self, q, inverse):
        assert inverse == False, "inverse query is not allowed for Generator2"
        ret_gen = self.func_gen(q)
        ret_random = self.func_random(q)
        if self.mode == 0:
            return ret_gen
        else:
            return ret_random