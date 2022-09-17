
SBOX = [
[5, 7, 4, 15, 3, 10, 13, 12, 9, 2, 8, 11, 6, 14, 0, 1, 3, 2, 13, 12, 1, 10, 11, 9, 7, 0, 4, 15, 14, 6, 8, 5, 5, 10, 7, 8, 9, 15, 1, 12, 4, 6, 3, 14, 2, 11, 13, 0, 9, 3, 10, 12, 8, 14, 5, 15, 2, 1, 0, 13, 11, 6, 4, 7],
[7, 13, 2, 9, 4, 6, 14, 10, 12, 8, 0, 15, 3, 1, 11, 5, 3, 5, 14, 4, 11, 10, 2, 1, 13, 8, 12, 15, 6, 7, 0, 9, 0, 10, 14, 4, 7, 1, 11, 12, 3, 5, 9, 13, 2, 8, 15, 6, 7, 2, 14, 1, 10, 12, 6, 0, 9, 13, 15, 5, 3, 11, 4, 8],
[5, 2, 15, 14, 13, 11, 4, 1, 12, 0, 8, 10, 3, 9, 7, 6, 10, 11, 6, 4, 15, 3, 1, 14, 9, 7, 2, 5, 12, 0, 13, 8, 1, 2, 12, 7, 0, 8, 3, 10, 4, 5, 15, 11, 13, 6, 14, 9, 10, 3, 9, 7, 4, 2, 12, 0, 5, 6, 14, 1, 13, 8, 11, 15],
[13, 14, 5, 7, 3, 1, 0, 10, 6, 2, 12, 9, 8, 11, 15, 4, 4, 3, 0, 1, 2, 14, 13, 12, 10, 5, 8, 11, 6, 7, 15, 9, 15, 2, 10, 1, 4, 7, 6, 3, 9, 5, 8, 13, 0, 11, 12, 14, 4, 8, 7, 11, 15, 13, 12, 0, 5, 2, 3, 14, 10, 6, 9, 1],
[1, 12, 3, 9, 14, 10, 2, 13, 15, 11, 6, 5, 7, 4, 8, 0, 7, 5, 6, 12, 0, 10, 15, 2, 4, 8, 13, 14, 1, 11, 9, 3, 7, 14, 0, 13, 1, 4, 5, 3, 11, 6, 12, 9, 10, 8, 15, 2, 3, 1, 5, 14, 9, 7, 0, 13, 8, 6, 2, 15, 11, 10, 4, 12],
[9, 2, 0, 14, 13, 3, 8, 15, 6, 5, 12, 7, 10, 11, 1, 4, 14, 8, 4, 9, 15, 0, 10, 1, 5, 12, 7, 6, 11, 2, 13, 3, 2, 5, 7, 15, 9, 4, 8, 0, 14, 3, 13, 12, 11, 1, 6, 10, 12, 5, 9, 15, 14, 3, 6, 2, 7, 0, 8, 11, 10, 4, 1, 13],
[13, 5, 3, 1, 10, 15, 6, 2, 14, 0, 11, 12, 7, 8, 4, 9, 0, 7, 12, 11, 6, 2, 9, 13, 5, 10, 3, 14, 4, 15, 1, 8, 9, 11, 2, 4, 7, 14, 10, 12, 15, 5, 13, 3, 8, 1, 6, 0, 4, 2, 9, 10, 3, 15, 1, 8, 6, 7, 11, 5, 13, 0, 14, 12],
[11, 8, 0, 15, 10, 1, 3, 12, 9, 6, 5, 4, 14, 7, 2, 13, 8, 11, 5, 12, 1, 6, 0, 2, 14, 7, 10, 13, 3, 15, 9, 4, 5, 13, 2, 0, 12, 1, 7, 4, 9, 6, 14, 10, 11, 8, 15, 3, 11, 10, 12, 6, 1, 8, 2, 13, 9, 14, 7, 3, 15, 0, 4, 5],
]

E = [31, 0, 1, 2, 3, 4, 3, 4, 5, 6, 7, 8, 7, 8, 9, 10, 11, 12, 11, 12, 13, 14, 15, 16, 15, 16, 17, 18, 19, 20, 19, 20, 21, 22, 23, 24, 23, 24, 25, 26, 27, 28, 27, 28, 29, 30, 31, 0]
P = [23, 16, 6, 22, 20, 24, 15, 5, 17, 30, 28, 14, 4, 29, 9, 31, 18, 13, 26, 0, 25, 2, 3, 10, 19, 7, 1, 8, 21, 12, 11, 27]
P_INV = [P.index(_) for _ in range(32)]
PC = [27, 9, 1, 44, 26, 15, 18, 8, 34, 40, 0, 29, 39, 41, 13, 3, 23, 42, 6, 45, 19, 32, 43, 30, 21, 38, 37, 5, 17, 22, 16, 25, 28, 14, 24, 11, 10, 12, 31, 4, 7, 20, 33, 46, 47, 35, 36, 2]

assert len(E) == 48
assert len(P) == 32 

def nsplit(s, n):
    return [s[k: k + n] for k in range(0, len(s), n)]

def s(x, i):
    row = ((x & 0b100000) >> 4) + (x & 1)
    col = (x & 0b011110) >> 1
    return SBOX[i][(row << 4) + col]

def p(x):
    x_bin = bin(x)[2:].rjust(32, '0')
    y_bin = [x_bin[P[i]] for i in range(len(P))]
    y = int(''.join([_ for _ in y_bin]), 2)
    return y

def p_inv(x):
    x_bin = bin(x)[2:].rjust(32, '0')
    y_bin = [x_bin[P_INV[i]] for i in range(32)]
    y = int(''.join([_ for _ in y_bin]), 2)
    return y

def e(x):
    x_bin = bin(x)[2:].rjust(32, '0')
    y_bin = [x_bin[E[i]] for i in range(len(E))]
    y = int(''.join([_ for _ in y_bin]), 2)
    return y

def F(x, k):
    x_in = bin(e(x) ^ k)[2:].rjust(48, '0')
    y_out = ''
    for i in range(0, 48, 6):
        x_in_i = int(x_in[i: i + 6], 2)
        y_out += bin(s(x_in_i, i // 6))[2:].rjust(4, '0')
    y_out = int(y_out, 2)
    y = p(y_out)
    return y

class Feistel():
    def __init__(self, key, rnd=10):
        self.key = key
        self.rnd = rnd
        self.keys = list()
        self.generatekeys(self.key)

    def generatekeys(self, key):
        if isinstance(key, bytes) or isinstance(key, bytearray):
            key = int(key.hex(), 16)
        self.keys.append(key)
        key_bin = bin(key)[2:].rjust(48, '0')
        l, r = key_bin[: 24], key_bin[24: ]
        for i in range(self.rnd - 1):
            l, r = l[1: ] + l[: 1], r[2: ] + r[: 2]        
            sub_key = ''.join([(l + r)[PC[j]] for j in range(48)])
            self.keys.append(int(sub_key, 2))

    def enc_block(self, x):
        x_bin = bin(x)[2:].rjust(64, '0')
        l, r = int(x_bin[: 32], 2), int(x_bin[32: ], 2)
        for i in range(self.rnd):
            l, r = r, l ^ F(r, self.keys[i])
        y = (l + (r << 32)) & ((1 << 64) - 1)
        return y

    def dec_block(self, x):
        x_bin = bin(x)[2:].rjust(64, '0')
        l, r = int(x_bin[: 32], 2), int(x_bin[32: ], 2)
        for i in range(self.rnd):
            l, r = r, l ^ F(r, self.keys[self.rnd - i - 1])
        y = (l + (r << 32)) & ((1 << 64) - 1)
        return y

    def encrypt(self, text):
        text_blocks = nsplit(text, 8)
        result = b""
        for block in text_blocks:
            block = int(block.hex(), 16)
            result += self.enc_block(block).to_bytes(8, 'big')
        return result

    def decrypt(self, text):
        text_blocks = nsplit(text, 8)
        result = b""
        for block in text_blocks:
            block = int(block.hex(), 16)
            result += self.dec_block(block).to_bytes(8, 'big')
        return result

if __name__ == "__main__":
    key = b'\xff' * 6
    pt = b'0123456789abcdef'
    feistel = Feistel(key, 4)
    ct = feistel.encrypt(pt)
    print(feistel.decrypt(ct) == pt)

