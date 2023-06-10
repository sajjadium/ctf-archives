import numpy as np
from functools import reduce

_cache = {
    "mul": {},
    "add": {}
}

class Element:
    
    A,B,C,D = [*map(lambda x: np.matrix(x, dtype=np.uint32), ([[1,0,0,0], [0,1,0,0], [0,0,0,1], [297,0,336,336]], [[1,269,0,0], [5,335,0,0], [0,8,0,1], [297,8,336,336]], [[8,0,0,0], [40,329,0,0], [232,0,295,0], [227,0,42,42]], [[329,0,269,0], [0,0,336,1], [105,0,8,0], [110,336,8,0]]
))]
    ID = np.matrix([[1,0,0,0], [0,1,0,0], [0,0,1,0], [0,0,0,1]], dtype=np.uint32)
    sz = 252
    mod = 337
    
    def __init__(self, x, _is_v = False):

        self._bytecache = None
        self._cachehash = None
        if _is_v:
            self.v = x
            return
        
        assert 0 <= x < self.sz
        a, x = x % 3, x // 3
        b, x = x % 3, x // 3
        c, x = x % 7, x // 7
        d = x
        self.v = reduce(lambda a,b: Element._mulmat(a,b), [
            Element._powmat(self.A, a),
            Element._powmat(self.B, b),
            Element._powmat(self.C, c),
            Element._powmat(self.D, d)
        ])
        
    @classmethod
    def _from_v(_, v):
        return Element(v, True)
        
    @staticmethod
    def _mulmat(A,B):
        return (A @ B) % Element.mod
    
    @staticmethod
    def _powmat(A,n):
        if n == 0: return Element.ID
        if n == 1: return A
        if n % 2:
            return Element._mulmat(A, Element._powmat(A, n-1))
        X = Element._powmat(A, n//2)
        return Element._mulmat(X, X)
    
    def to_byte(self):
        if self._bytecache is None:
            self._bytecache = MAPPING[hash(self)]
        return self._bytecache
    
    def __add__(self, other):
        key = (self.to_byte(), other.to_byte())
        r = _cache["add"].get(key)
        if r: return r
        r = Element._from_v(Element._mulmat(self.v, other.v))
        _cache["add"][key] = r
        return r
    
    def __mul__(self, n):
        key = (self.to_byte(), n)
        r = _cache["mul"].get(key)
        if r: return r
        r = Element._from_v(Element._powmat(self.v, n))
        _cache["mul"][key] = r
        return r
    
    def __rmul__(self, n):
        return self*n
    
    def __hash__(self):
        if self._cachehash is None:
            self._cachehash = hash(bytes(np.ravel(self.v)))
        return self._cachehash
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __str__(self):
        return str(self.to_byte())
    
    def __repr__(self):
        return f"<E:{self}>"
    
MAPPING = {hash(Element(i)): i for i in range(Element.sz)}