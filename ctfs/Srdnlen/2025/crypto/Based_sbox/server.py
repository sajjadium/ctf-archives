import os, xoflib, functools, signal


def sbox(x, n=64):
    mods = {64: 0x1b, 128: 0x87}

    mod = mods[n]

    def mul(a, b, n=64):
        r = 0
        for i in range(n):
            r <<= 1
            if r & (1 << n):
                r ^= (1 << n) | mod
            if a & (1 << (n - 1 - i)):
                r ^= b
        return r
    
    def pow(x, e, n=64):
        if e < 0:
            raise ValueError("e must be non-negative")
        if e == 0:
            return 1
        if e == 1:
            return x
        r = pow(x, e >> 1)
        r = mul(r, r, n=n)
        if e & 1:
            r = mul(r, x, n=n)
        return r
    
    return (pow(x, (1 << n) - 2) ^ 0x01d_5b ^ 0x_15_ba5ed) & ((1 << n) - 1)


class Feistel:
    def __init__(self, key: bytes, rounds=10, block_size=16) -> None:
        assert len(key) == block_size // 2
        assert block_size % 2 == 0
        self._rounds = rounds
        self._block_size = block_size
        self._expand_key(key)
    
    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return bytes(x ^ y for x, y in zip(a, b))
    
    @staticmethod
    def _pad(m: bytes, n: int) -> bytes:
        x = n - len(m) % n
        return m + bytes([x] * x)
    
    @staticmethod
    def _unpad(m: bytes, n: int) -> bytes:
        x = m[-1]
        if not 1 <= x <= n:
            raise ValueError("invalid padding")
        return m[:-x]

    def _expand_key(self, key: bytes) -> None:
        share_xof = xoflib.shake256(key)
        shares = [share_xof.read(self._block_size // 2) for _ in range(self._rounds - 1)]
        shares.append(self.xor(functools.reduce(self.xor, shares), key))
        self._round_keys = [int.from_bytes(share, "big") for share in shares]
        assert len(self._round_keys) == self._rounds
    
    def _f(self, l: int, r: int, key: int) -> int:
        return l ^ sbox(r ^ key, n=self._block_size * 4)
    
    def _encrypt_block(self, pt: bytes) -> bytes:
        assert len(pt) == self._block_size
        l, r = int.from_bytes(pt[:self._block_size // 2], "big"), int.from_bytes(pt[self._block_size // 2:], "big")
        for i in range(self._rounds):
            l, r = r, self._f(l, r, self._round_keys[i])
        ct = l.to_bytes(self._block_size // 2, "big") + r.to_bytes(self._block_size // 2, "big")
        return ct
    
    def _decrypt_block(self, ct: bytes) -> bytes:
        assert len(ct) == self._block_size
        l, r = int.from_bytes(ct[:self._block_size // 2], "big"), int.from_bytes(ct[self._block_size // 2:], "big")
        for i in reversed(range(self._rounds)):
            l, r = self._f(r, l, self._round_keys[i]), l
        pt = l.to_bytes(self._block_size // 2, "big") + r.to_bytes(self._block_size // 2, "big")
        return pt
    
    def encrypt(self, pt: bytes) -> bytes:
        pt = self._pad(pt, self._block_size)
        ct = os.urandom(self._block_size)
        for i in range(0, len(pt), self._block_size):
            ct += self._encrypt_block(self.xor(pt[i:i + self._block_size], ct[-self._block_size:]))
        return ct
    
    def decrypt(self, ct: bytes) -> bytes:
        if len(ct) % self._block_size != 0:
            raise ValueError("ciphertext length must be a multiple of block size")
        pt = b""
        for i in range(0, len(ct) - self._block_size, self._block_size):
            pt += self.xor(self._decrypt_block(ct[i + self._block_size:i + self._block_size * 2]), ct[i:i + self._block_size])
        return self._unpad(pt, self._block_size)


if __name__ == "__main__":
    signal.alarm(240)
    
    key = os.urandom(8)
    cipher = Feistel(key, rounds=7, block_size=16)

    pt = (  # ChatGPT cooked a story for us
        "Once upon a time, after linear and differential cryptanalysis had revolutionized the cryptographic landscape, "
        "and before Rijndael was selected as the Advanced Encryption Standard (AES), the field of cryptography was in a unique state of flux. "
        "New cryptanalytic methods exposed vulnerabilities in many established ciphers, casting doubt on the long-term security of systems "
        "once thought to be invulnerable. In response, the U.S. National Institute of Standards and Technology (NIST) "
        "launched a competition to find a successor to the aging DES. In 2000, Rijndael was chosen, setting a new standard for secure encryption. "
        "But even as AES became widely adopted, new challenges, like quantum computing, loomed on the horizon."
    ).encode()
    ct = cipher.encrypt(pt)
    print(ct.hex())

    guess = bytes.fromhex(input("guess: "))
    if guess == key:
        flag = os.getenv("FLAG", "srdnlen{this_is_a_fake_flag}")
        print(flag)
    else:
        print("srdnlen{wrong_guess}")
