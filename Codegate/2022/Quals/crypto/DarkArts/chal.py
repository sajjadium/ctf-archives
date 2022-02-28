import os
import hashlib 
import signal 

signal.alarm(300)

def inner_product(u, v):
    assert len(u) == len(v)
    res = 0
    for a, b in zip(u, v):
        res += a * b
    return res

def guess_mode(G):
    while True:
        idx = int(input())
        if idx == 0:
            x = int(input())
            print(G.calc(x))
        elif idx == 1:
            mode = int(input())
            if mode != G.mode:
                exit()
            else:
                break
        else:
            exit()

def guess_key(G, l):
    while True:
        idx = int(input())
        if idx == 0:
            x = int(input())
            print(G.func_gen(x))
        elif idx == 1:
            for i in range(l):
                x = int(input())
                if x != G.key[i]:
                    exit()
            break
        else:
            exit()

class Generator1:
    def __init__(self):
        seed = int.from_bytes(os.urandom(32), "big")
        self.key = [0] * 256
        for i in range(256):
            self.key[i] = (seed >> i) & 1
        self.mode = os.urandom(1)[0] & 1
        
        self.p = 2
        self.q = 3

        self.cache0 = {}
        self.cache1 = {}
        
    def func_gen(self, x):
        assert 0 <= x < (1 << 256)
        if x in self.cache0.keys():
            return self.cache0[x]
        arr = [0] * 256
        for i in range(256):
            arr[i] = (x >> i) & 1
        prod = inner_product(self.key, arr)
        self.cache0[x] = (prod % self.p + prod % self.q) % self.p
        return self.cache0[x]
    
    def func_random(self, x):
        assert 0 <= x < (1 << 256)
        if x in self.cache1.keys():
            return self.cache1[x]
        self.cache1[x] = os.urandom(1)[0] & 1
        return self.cache1[x]
    
    def calc(self, x):
        ret0 = self.func_gen(x)
        ret1 = self.func_random(x)
        if self.mode == 0:
            return ret0
        else:
            return ret1

def challenge_generator_1():
    print("Challenge 1")
    for _ in range(64):
        G = Generator1()
        guess_mode(G)

class Generator2:
    def __init__(self):
        seed = int.from_bytes(os.urandom(32), "big")
        self.key = [0] * 256
        for i in range(256):
            self.key[i] = (seed >> i) & 1
        self.mode = os.urandom(1)[0] & 1
        
        self.p = 5
        self.q = 7

        self.cache0 = {}
        self.cache1 = {}
    
    def func_gen(self, x):
        x = int.from_bytes(hashlib.sha256(str(x).encode()).digest(), "big")
        if x in self.cache0.keys():
            return self.cache0[x]
        hashed = [0] * 256
        for i in range(256):
            hashed[i] = (x >> i) & 1
        prod = inner_product(self.key, hashed)
        self.cache0[x] = (prod % self.p + prod % self.q) % self.p
        return self.cache0[x]
    
    def func_random(self, x):
        x = int.from_bytes(hashlib.sha256(str(x).encode()).digest(), "big")
        if x in self.cache1.keys():
            return self.cache1[x]
        self.cache1[x] = int.from_bytes(os.urandom(32), "big") % self.p
        return self.cache1[x]
    
    def calc(self, x):
        ret0 = self.func_gen(x)
        ret1 = self.func_random(x)
        if self.mode == 0:
            return ret0
        else:
            return ret1

def challenge_generator_2():
    print("Challenge 2")
    for _ in range(64):
        G = Generator2()
        guess_mode(G)

class Generator3:
    def __init__(self):
        seed = int.from_bytes(os.urandom(16), "big")
        self.key = [0] * 64
        for i in range(64):
            self.key[i] = seed & 3
            seed = seed >> 2

        self.p = 2
        self.q = 5
    
    def func_gen(self, x):
        x = int.from_bytes(hashlib.sha256(str(x).encode()).digest(), "big")
        hashed = [0] * 64
        for i in range(64):
            hashed[i] = x % self.q
            x = x // self.q
        prod = inner_product(self.key, hashed)
        return (prod % self.q) % self.p

def challenge_generator_3():
    print("Challenge 3")
    G = Generator3()
    guess_key(G, 64)

class Generator4:
    def __init__(self):
        self.key = [0] * 16
        for i in range(16):
            self.key[i] = int.from_bytes(os.urandom(32), "big")

        self.p = int.from_bytes(os.urandom(32), "big") + (1 << 256)
        self.q = int.from_bytes(os.urandom(16), "big") + (1 << 128)
        
        print(self.p)
        print(self.q)
    
    def func_gen(self, x):
        x = hashlib.sha256(str(x).encode()).digest()
        hashed = []
        for _ in range(16):
            hashed.append(int.from_bytes(x, "big"))
            x = hashlib.sha256(x).digest()
        prod = inner_product(self.key, hashed)
        return (prod % self.p + prod % self.q) % self.p

def challenge_generator_4():
    print("Challenge 4")
    G = Generator4()
    guess_key(G, 16)

challenge_generator_1()
challenge_generator_2()
challenge_generator_3()
challenge_generator_4()

flag = open("flag", "r").read()
print(flag)