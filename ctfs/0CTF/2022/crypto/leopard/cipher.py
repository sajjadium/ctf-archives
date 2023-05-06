def pad(s):
    l = 8 - (len(s) % 8)
    return s + l * bytearray([l])

def unpad(s):
    assert s[-1] <= 8
    return s[: -s[-1]]

def gmul(a, b):
    c = 0
    while a and b:
        if b & 1:
            c ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11d
        b >>= 1
    return c

def gen_sbox():
    """
    SBOX is generated in a similar way as AES, i.e., linear transform over the multiplicative inverse (L * x^-1 + C),
    to prevent differential fault analysis.
    """
    
    INV = [0, 1, 142, 244, 71, 167, 122, 186, 173, 157, 221, 152, 61, 170, 93, 150, 216, 114, 192, 88, 224, 62, 76, 102, 144, 222, 85, 128, 160, 131, 75, 42, 108, 237, 57, 81, 96, 86, 44, 138, 112, 208, 31, 74, 38, 139, 51, 110, 72, 137, 111, 46, 164, 195, 64, 94, 80, 34, 207, 169, 171, 12, 21, 225, 54, 95, 248, 213, 146, 78, 166, 4, 48, 136, 43, 30, 22, 103, 69, 147, 56, 35, 104, 140, 129, 26, 37, 97, 19, 193, 203, 99, 151, 14, 55, 65, 36, 87, 202, 91, 185, 196, 23, 77, 82, 141, 239, 179, 32, 236, 47, 50, 40, 209, 17, 217, 233, 251, 218, 121, 219, 119, 6, 187, 132, 205, 254, 252, 27, 84, 161, 29, 124, 204, 228, 176, 73, 49, 39, 45, 83, 105, 2, 245, 24, 223, 68, 79, 155, 188, 15, 92, 11, 220, 189, 148, 172, 9, 199, 162, 28, 130, 159, 198, 52, 194, 70, 5, 206, 59, 13, 60, 156, 8, 190, 183, 135, 229, 238, 107, 235, 242, 191, 175, 197, 100, 7, 123, 149, 154, 174, 182, 18, 89, 165, 53, 101, 184, 163, 158, 210, 247, 98, 90, 133, 125, 168, 58, 41, 113, 200, 246, 249, 67, 215, 214, 16, 115, 118, 120, 153, 10, 25, 145, 20, 63, 230, 240, 134, 177, 226, 241, 250, 116, 243, 180, 109, 33, 178, 106, 227, 231, 181, 234, 3, 143, 211, 201, 66, 212, 232, 117, 127, 255, 126, 253]
    L = [[0, 0, 1, 1, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 0],
    [1, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 1, 0, 1, 0]]
    C = [1, 0, 1, 1, 1, 0, 1, 0]
    S = []
    for _ in range(256):
        inv = bin(INV[_])[2:].rjust(8, '0')[::-1]
        v = [sum([a * int(b) for (a, b) in zip(L[__], inv)] + [C[__]]) % 2 for __ in range(8)]
        S.append(sum([v[__] * 2**(7 - __) for __ in range(8)]))
    return S

class AEAD:
    IDX = [6, 7, 15, 16, 24, 25, 34, 35]
    SBOX = gen_sbox()
    SKIP = 4

    def __init__(self, key: bytes, iv: bytes, fault=False):
        assert len(key) == 16
        assert len(iv) == 16
        self.init_state(key, iv)
        self.fault = fault

    def init_state(self, key, iv):
        self.state = list(key + iv)
        self.state += [_ ^ 0xff for _ in key[: 3]]
        self.state += [0xef]
        self.update(1337)

    def update(self, n=1):
        for _ in range(n):
            P = self.state[  :  8]
            Q = self.state[ 8: 17]
            R = self.state[17: 26]
            S = self.state[26: ]

            P_ = ord('0') ^ P[0] ^ P[2] ^ P[3] ^ gmul(P[4], P[6]) ^ Q[5]
            Q_ = ord('C') ^ Q[0] ^ Q[3] ^ gmul(Q[1], Q[8]) ^ gmul(R[4], S[6])
            R_ = ord('T') ^ R[0] ^ R[2] ^ R[3] ^ gmul(R[5], R[8]) ^ S[7]
            S_ = ord('F') ^ S[0] ^ S[8] ^ gmul(S[2], S[4]) ^ gmul(P[7], Q[2])

            self.state = P[1:] + [self.SBOX[P_]] + \
            Q[1:] + [self.SBOX[Q_]] + \
            R[1:] + [self.SBOX[R_]] + \
            S[1:] + [self.SBOX[S_]]

    def process_ad(self, ad):
        ad = pad(ad)
        for i in range(len(ad) // 8):
            tmp = ad[8 * i: 8 * i + 8]
            for _ in range(8):
                self.state[self.IDX[_]] ^= tmp[_]
            self.update(self.SKIP)

    def process_pt(self, pt, flag):
        if flag == 0:
            pt = pad(pt)
        ct = []
        for i in range(len(pt) // 8): 
            tmp = pt[8 * i: 8 * i + 8]
            for _ in range(8):
                if flag == 0:
                    self.state[self.IDX[_]] ^= tmp[_]
                    ct.append(self.state[self.IDX[_]])
                else:
                    ct.append(self.state[self.IDX[_]] ^ tmp[_])
                    self.state[self.IDX[_]] = tmp[_]
            if self.fault and i == len(pt) // 16 - 1:
                self.state[0] ^= 0xff
            if i + 1 != len(pt) // 8:
                self.update(self.SKIP)
        return bytes(ct)

    def generate_tg(self):
        self.update(137)
        tg = []
        for i in range(2):
            for _ in range(8):
                tg.append(self.state[self.IDX[_]])
            self.update(self.SKIP)
        return bytes(tg)

    def encrypt(self, pt, ad):
        self.process_ad(ad)
        ct = self.process_pt(pt, 0)
        tg = self.generate_tg()
        return ct, tg

    def decrypt(self, ct, ad, tg):
        self.process_ad(ad)
        pt = self.process_pt(ct, 1)
        tg_ = self.generate_tg()
        if tg_ != tg:
            return None
        else:
            return unpad(pt)

if __name__ == "__main__":
    key = b'\xff' * 16
    iv = b'\xee' * 16
    msg = b'\xdd' * 16
    ad = b'\xcc' * 16
    C = AEAD(key, iv)
    ct, tg = C.encrypt(msg, ad)
    C = AEAD(key, iv)
    assert C.decrypt(ct, ad, tg) == msg
