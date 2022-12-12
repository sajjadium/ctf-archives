from LFSR import LFSR
from ctypes import c_uint64
from util import aes, nsplit
from Crypto.Util.Padding import pad


class Derek():
    def __init__(self, key, rnd=10):
        self.key = key
        self.rnd = rnd
        self.keys = list()
        self.generatekeys(self.key)

    def generatekeys(self, key: bytes) -> None:
        lfsr = LFSR(int.from_bytes(key, 'big'))
        for i in range(self.rnd):
            b = 0
            for j in range(128):
                b = (b << 1) + lfsr.next()
            self.keys.append(b.to_bytes(16, 'big'))

    def enc_block(self, x: int) -> int:
        x_bin = bin(x)[2:].rjust(128, '0')
        l, r = int(x_bin[:64], 2), int(x_bin[64:], 2)
        for i in range(self.rnd):
            magic = c_uint64(0xffffffffffffffff)
            for m in bytes([int(bin(byte)[2::].zfill(8)[8::-1], 2)
                            for byte in l.to_bytes(8, 'big')]):
                magic.value ^= c_uint64(m << 56).value
                for j in range(8):
                    if magic.value & 0x8000000000000000 != 0:
                        magic.value = magic.value << 1 ^ 0x1b
                    else:
                        magic.value = magic.value << 1
            magic.value ^= 0xffffffffffffffff
            t = bytes([int(bin(byte)[2::].zfill(8)[8::-1], 2)
                      for byte in bytes(magic)])
            t = aes(int(t.hex(), 16), self.keys[i]) & 0xffffffffffffffff
            t ^= aes(0xdeadbeefbaadf00d if i % 2 else 0xbaadf00ddeadbeef,
                     self.keys[i]) & 0xffffffffffffffff
            l, r = r ^ t, l
        l ^= int.from_bytes(self.key[:8], 'big')
        r ^= int.from_bytes(self.key[8:], 'big')
        l, r = r, l
        y = (l + (r << 64)) & 0xffffffffffffffffffffffffffffffff
        return y

    def dec_block(self, x: int) -> int:
        raise Exception('Unimplement')

    def encrypt(self, text: bytes) -> bytes:
        text_blocks = nsplit(pad(text, 16), 16)
        result = b''
        for block in text_blocks:
            block = int.from_bytes(block, 'big')
            result += self.enc_block(block).to_bytes(16, 'big')
        return result

    def decrypt(self, text: bytes) -> bytes:
        raise Exception('Unimplement')
