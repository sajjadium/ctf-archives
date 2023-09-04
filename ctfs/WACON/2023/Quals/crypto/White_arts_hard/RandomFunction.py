import os

class RandomFunction():    
    def __init__(self, n):
        self.domain_cache = {}
        self.range_cache = {}
        self.n = n # n "bytes"

    # Inverse query is not allowed
    def query(self, q):
        x = q
        if x not in self.domain_cache:
            self.domain_cache[x] = os.urandom(self.n)
        return self.domain_cache[x]