from flag import flag
import os

assert flag[:4] == b"wwf{" and flag[-1:] == b"}"

class LFSRHamster:
    def __init__(self, key):
        self.state = [int(eb) for b in key for eb in bin(b)[2:].zfill(8)]
        self.taps = [0, 1, 2, 7]
        self.filter = [85, 45, 76, 54, 45, 35, 39, 37, 117, 13, 112, 64, 75, 117, 21, 40]

        for _ in range(128):
            self.clock()

    def xorsum(self, l):
        s = 0
        for x in l:
            s ^= x
        return s
    
    def hamster(self, l):
        return l[min(sum(l), len(l) - 1)]

    def clock(self):
        x = [self.state[i] for i in self.filter]
        self.state = self.state[1:] + [self.xorsum(self.state[p] for p in self.taps)]
        return self.hamster(x)
    
    def encrypt(self, data):
        c = []
        for p in data:
            b = 0
            for _ in range(8):
                b = (b << 1) | self.clock()
            c += [p ^ b]
        return bytes(c)
    
if __name__ == "__main__":    
    H = LFSRHamster(os.urandom(16))

    while True:
        t = input(">")
        if t == "flag":
            print(H.encrypt(flag).hex())
        elif t == "enc":
            p = bytes.fromhex(input(">"))
            print(H.encrypt(p).hex())