from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from secrets import token_hex


class CipherG(object):

    ROUNDS = 64
    S1 = [3, 5, 11, 12, 15, 7, 1, 13, 2, 0, 10, 9, 6, 14, 4, 8]
    S2 = [8, 12, 15, 13, 4, 5, 9, 1, 7, 3, 0, 2, 11, 10, 6, 14]

    def __init__(self, key: int):
        self.key = key
        self.key_schedule = [(self.key >> (24 - 8 * i)) & 0xFF for i in range(0, 4)]

    def _encrypt_round(self, x: int, k: int) -> int:
        u = x ^ k
        u1, u2 = (u >> 4) & 0x0F, u & 0x0F
        u1, u2 = self.S1[u1], self.S2[u2]
        u = ((u1 << 4) + u2) & 0xFF
        return ((u << 3) | (u >> 5)) & 0xFF

    def _encrypt_feistel(self, x: int) -> int:
        y1, y2 = (x >> 8) & 0xFF, x & 0xFF
        for i in range(0, self.ROUNDS):
            y1, y2 = y2, y1 ^ self._encrypt_round(y2, self.key_schedule[i % 4])
        return ((y2 << 8) + y1) & 0xFFFF

    def encrypt(self, x: bytearray) -> bytearray:
        x += bytearray([0x00] * (len(x) % 2))
        for i in range(0, len(x) // 2):
            current_block = ((x[i * 2] << 8) + x[i * 2 + 1]) & 0xFFFF
            current_block = self._encrypt_feistel(current_block)
            x[i * 2], x[i * 2 + 1] = (current_block >> 8) & 0xFF, current_block & 0xFF
        return x


if __name__ == '__main__':

    with open('../dev/flag.txt', 'r') as f:
        flag = bytes(f.readline(), 'ascii')

    with open('../dev/key.txt', 'r') as f:
        key1 = int(f.readline(), 16) & 0x0FFFFFFF
        key2 = int(f.readline(), 16) & 0x0FFFFFFF

    cipher_1 = CipherG(key1)
    cipher_2 = CipherG(key2)

    pt_str = '65fe13fed92adbc9'
    ct = cipher_2.encrypt(cipher_1.encrypt(bytearray.fromhex(pt_str)))
    ct_str = ct.hex()

    salt = token_hex(64)
    aes_key = SHA256.new((salt + hex(key1)[2:] + hex(key2)[2:]).encode()).digest()
    aes = AES.new(aes_key, AES.MODE_CTR)

    with open('task.txt', 'w') as f:
        f.write(aes.encrypt(flag).hex() + '\n')
        f.write(aes.nonce.hex() + '\n')
        f.write(salt + '\n')
        f.write(pt_str + '\n')
        f.write(ct_str + '\n')
