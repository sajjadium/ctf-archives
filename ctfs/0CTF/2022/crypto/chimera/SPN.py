from copy import deepcopy 

S_BOX = [47, 13, 50, 214, 119, 149, 138, 113, 200, 93, 180, 247, 86, 189, 125, 97, 226, 249, 159, 168, 55, 118, 169, 178, 18, 49, 102, 65, 34, 231, 10, 192, 100, 122, 75, 177, 205, 29, 40, 124, 103, 131, 232, 234, 72, 114, 127, 66, 154, 243, 27, 236, 106, 181, 87, 129, 38, 26, 140, 151, 135, 73, 171, 239, 132, 95, 184, 148, 48, 4, 203, 183, 250, 44, 57, 0, 46, 158, 233, 161, 217, 39, 126, 210, 53, 215, 21, 9, 139, 68, 209, 248, 5, 242, 42, 79, 212, 7, 71, 155, 61, 251, 134, 199, 152, 80, 16, 111, 82, 81, 123, 12, 216, 94, 142, 146, 204, 172, 92, 147, 1, 186, 85, 230, 108, 221, 36, 246, 206, 59, 52, 37, 33, 153, 136, 45, 20, 98, 228, 188, 117, 245, 6, 223, 83, 17, 91, 207, 54, 160, 175, 220, 133, 28, 156, 3, 77, 15, 237, 89, 56, 30, 225, 202, 24, 193, 121, 227, 120, 174, 25, 201, 32, 96, 110, 252, 219, 70, 51, 255, 238, 74, 150, 170, 104, 213, 187, 244, 165, 2, 163, 11, 235, 253, 116, 191, 211, 176, 179, 19, 195, 22, 143, 62, 173, 190, 78, 222, 112, 254, 23, 208, 241, 196, 198, 240, 101, 41, 128, 144, 162, 69, 109, 60, 137, 197, 76, 8, 229, 84, 88, 141, 145, 164, 90, 166, 157, 67, 185, 115, 224, 35, 167, 130, 99, 14, 182, 43, 105, 194, 58, 64, 31, 218, 63, 107]
S_BOX_INV = [S_BOX.index(_) for _ in range(len(S_BOX))]

MIX_BOX = [[1, 3, 3, 7], [7, 1, 3, 3], [3, 7, 1, 3], [3, 3, 7, 1]]
MIX_BOX_INV = [[234, 86, 195, 4], [4, 234, 86, 195], [195, 4, 234, 86], [86, 195, 4, 234]]

RCON = [
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
]

def GF2_mul(a, b):
    p = 0
    for i in range(8):
        lsb = b & 1
        b = b >> 1
        if lsb:
            p = p ^ a
        lsb = a & 0x80
        a = (a << 1) & 0xff
        if lsb:
            a = a ^ 0x1B
    return p

def nsplit(s, n):
    return [s[k: k + n] for k in range(0, len(s), n)]

def text2row(text):
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix[i][j] = text[4 * j + i]
    return matrix

def row2text(matrix):
    text = 0
    for i in range(4):
        for j in range(4):
            text |= (matrix[i][j] << (120 - 8 * (i + 4 * j)))
    return text.to_bytes(16, 'big')

def subBytes(block):
    for i in range(4):
        for j in range(4):
            block[i][j] = S_BOX[block[i][j]]
    return block
    
def shiftRows(block):
    for i in range(4):
        block[i] = block[i][i:] + block[i][:i]
    return block

def addRoundKey(block1, block2):
    result = [[ 0 for i in range(4)] for j in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = block1[i][j] ^ block2[j][i]
    return result

def xor_all(array):
    result = array[0]
    for i in range(1, len(array)):
        result ^= array[i]
    return result

def mixColumns(block):
    result = []
    for i in range(4):
        tmp = []
        for j in range(4):
            x = xor_all([GF2_mul(MIX_BOX[i][m], block[m][j]) for m in range(4)])
            tmp.append(x)
        result.append(tmp)
    return result

def subBytes_inv(block):
    for i in range(4):
        for j in range(4):
            block[i][j] = S_BOX_INV[block[i][j]]
    return block
    
def shiftRows_inv(block):
    for i in range(4):
        block[i] = block[i][-i:] + block[i][:-i]
    return block    

def mixColumns_inv(block):
    result = []
    for i in range(4):
        tmp = []
        for j in range(4):
            x = xor_all([GF2_mul(MIX_BOX_INV[i][m], block[m][j]) for m in range(4)])
            tmp.append(x)
        result.append(tmp)
    return result

class SPN():
    def __init__(self, key, rnd=10):
        self.key = key
        self.rnd = rnd
        self.keys = list()
        self.generatekeys()
        
    def generatekeys(self):
        block = [self.key[i:i+4] for i in range(0, 16, 4)]
        self.keys.append(block)
        for i in range(1, 1 + self.rnd):
            self.keys.append([])
            tmp = self.keys[i - 1][3]
            tmp = tmp[1:] + tmp[:1]
            tmp = [S_BOX[_] for _ in tmp]
            tmp[0] ^= RCON[i]
            for j in range(4):  
                for k in range(4):
                    if j == 0:
                        tmp[k] ^= self.keys[i - 1][j][k]
                    else:
                        tmp[k] = self.keys[i - 1][j][k] ^ self.keys[i][j - 1][k]
                self.keys[i].append(deepcopy(tmp))

    def encrypt(self, text):
        text_blocks = nsplit(text, 16)
        result = b""
        for block in text_blocks:
            block = text2row(block)
            block = addRoundKey(block, self.keys[0])
            for i in range(self.rnd):
                block = subBytes(block)
                if i != 0:
                    block = shiftRows(block)
                if i != self.rnd - 1:
                    block = mixColumns(block)
                block = addRoundKey(block, self.keys[i + 1])
            result += row2text(block)
        return result
    
    def decrypt(self, text):
        text_blocks = nsplit(text, 16)
        result = b""
        for block in text_blocks:
            block = text2row(block)
            for i in range(self.rnd):
                block = addRoundKey(block, self.keys[self.rnd - i])
                if i != 0:
                    block = mixColumns_inv(block)
                if i != self.rnd - 1:
                    block = shiftRows_inv(block)
                block = subBytes_inv(block)
            block = addRoundKey(block, self.keys[0])
            result += row2text(block)
        return result


if __name__ == "__main__":
    key = b'\xff' * 16
    pt = b'0123456789abcdef'
    spn = SPN(key, 4)
    ct = spn.encrypt(pt)
    print(spn.decrypt(ct) == pt)
