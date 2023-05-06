from dataclasses import dataclass
from functools import reduce

@dataclass
class register:
    name: str
    val:  int
    mid:  int
    mask: int
    taps: int
    out:  int
        
def parity(r):
    cn = 0
    while r:
        r &= (r - 1)
        cn += 1
    return cn & 1

class LFSR:
    def __init__(self, key, iv):
        self.r1 = register('r1', 0, 0x000100, 0x07FFFF, 0x072000, 0x040000)
        self.r2 = register('r2', 0, 0x000400, 0x3FFFFF, 0x300000, 0x200000)
        self.r3 = register('r3', 0, 0x000400, 0x7FFFFF, 0x700080, 0x400000)
        self.mem = (self.r1, self.r2, self.r3)
        self.setup(key, iv)
        
    def majority(self):
        res = 0
        for reg in self.mem:
            res += parity(reg.val & reg.mid)
        return res
    
    def clockone(self, reg):
        t = reg.val & reg.taps
        reg.val <<= 1
        reg.val &= reg.mask
        reg.val |= parity(t)
    
    def clockall(self):
        for reg in self.mem:
            self.clockone(reg)

    def clock(self):
        maj = self.majority()
        for reg in self.mem:
            if (reg.val & reg.mid != 0) <= maj:
                self.clockone(reg)
    
    def getbit(self):
        self.clock()
        res = 0
        for reg in self.mem:
            res ^= parity(reg.val & reg.out)
        return res
    
    def setup(self, key, iv = 0):
        for i in range(64):
            self.clockall()
            kbit = (key[i >> 3] >> (i & 7)) & 1
            for reg in self.mem:
                reg.val ^= kbit

        for i in range(22):
            self.clockall()
            fbit = (iv >> i) & 1
            for reg in self.mem:
                reg.val ^= fbit

        for i in range(100):
            self.clock()