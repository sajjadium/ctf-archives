import os

class RandomPermutation():    
    def __init__(self, n):
        self.domain_cache = {}
        self.range_cache = {}
        self.n = n # n "bytes"

    def query(self, q, inverse = False):
        if not inverse:
            x = q
            if x in self.domain_cache:
                return self.domain_cache[x]
            
            while True:
                y = os.urandom(self.n)
                if y in self.range_cache:
                    continue

                self.domain_cache[x] = y
                self.range_cache[y] = x    
                return y

        else:
            y = q
            if y in self.range_cache:
                return self.range_cache[y]
            
            while True:
                x = os.urandom(self.n)
                if x in self.domain_cache:
                    continue

                self.domain_cache[x] = y
                self.range_cache[y] = x    
                return x        