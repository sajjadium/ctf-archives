from SPN import SPN
from Feistel import Feistel

def nsplit(s, n):
    return [s[k: k + n] for k in range(0, len(s), n)]

P = [3 * _ % 16 for _ in range(16)]
P_INV = [P.index(_) for _ in range(16)]

class Chimera():
    def __init__(self, key, rnd=4):
        self.key = key
        self.C1a = Feistel(key[: 6], rnd)
        self.C1b = Feistel(key[6: 12], rnd)
        self.C2 = SPN(key, rnd)

    def encrypt(self, text):
        text_blocks = nsplit(text, 16)
        result = b""
        for block in text_blocks:
            block_l = block[: 8]
            block_r = block[8: ]
            mid = self.C1a.encrypt(block_l) + self.C1b.encrypt(block_r)
            mid = bytearray([mid[i] for i in P])
            result += self.C2.encrypt(mid)
        return result

    def decrypt(self, text):
        text_blocks = nsplit(text, 16)
        result = b""
        for block in text_blocks:
            mid = self.C2.decrypt(block)
            mid = bytearray([mid[i] for i in P_INV])
            block_l = mid[: 8]
            block_r = mid[8: ]
            pt = self.C1a.decrypt(block_l) + self.C1b.decrypt(block_r)
            result += pt
        return result

if __name__ == "__main__":
    key = b'\xff' * 16
    pt = b'0123456789abcdef'
    chimera = Chimera(key, 4)
    ct = chimera.encrypt(pt)
    print(chimera.decrypt(ct) == pt)