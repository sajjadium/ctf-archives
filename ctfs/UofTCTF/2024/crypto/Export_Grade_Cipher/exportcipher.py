import os

class LFSR:
    def __init__(self, seed, taps, size):
        assert seed != 0
        assert (seed >> size) == 0
        assert len(taps) > 0 and (size - 1) in taps
        self.state = seed
        self.taps = taps
        self.mask = (1 << size) - 1

    def _shift(self):
        feedback = 0
        for tap in self.taps:
            feedback ^= (self.state >> tap) & 1
        self.state = ((self.state << 1) | feedback) & self.mask
    
    def next_byte(self):
        val = self.state & 0xFF
        for _ in range(8):
            self._shift()
        return val


class ExportGradeCipher:
    def __init__(self, key):
        # 40 bit key
        assert (key >> 40) == 0
        self.key = key
        self.initialized = False
    
    def init_with_nonce(self, nonce):
        # 256 byte nonce, nonce size isnt export controlled so hopefully this will compensate for the short key size
        assert len(nonce) == 256
        self.lfsr17 = LFSR((self.key & 0xFFFF) | (1 << 16), [2, 9, 10, 11, 14, 16], 17)
        self.lfsr32 = LFSR(((self.key >> 16) | 0xAB << 24) & 0xFFFFFFFF, [1, 6, 16, 21, 23, 24, 25, 26, 30, 31], 32)
        self.S = [i for i in range(256)]
        # Fisher-Yates shuffle S-table
        for i in range(255, 0, -1): 
            # generate j s.t. 0 <= j <= i, has modulo bias but good luck exploiting that
            j = (self.lfsr17.next_byte() ^ self.lfsr32.next_byte()) % (i + 1)
            self.S[i], self.S[j] = self.S[j], self.S[i]
        j = 0
        # use nonce to scramble S-table some more
        for i in range(256):
            j = (j + self.lfsr17.next_byte() ^ self.lfsr32.next_byte() + self.S[i] + nonce[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
        self.S_inv = [0 for _ in range(256)]
        for i in range(256):
            self.S_inv[self.S[i]] = i
        self.initialized = True
    
    def _update(self, v):
        i = self.lfsr17.next_byte() ^ self.lfsr32.next_byte()
        self.S[v], self.S[i] = self.S[i], self.S[v]
        self.S_inv[self.S[v]] = v
        self.S_inv[self.S[i]] = i
    
    def encrypt(self, msg):
        assert self.initialized
        ct = bytes()
        for v in msg:
            ct += self.S[v].to_bytes()
            self._update(v)
        return ct
    
    def decrypt(self, ct):
        assert self.initialized
        msg = bytes()
        for v in ct:
            vo = self.S_inv[v]
            msg += vo.to_bytes()
            self._update(vo)
        return msg


if __name__ == "__main__":
    cipher = ExportGradeCipher(int.from_bytes(os.urandom(5)))
    nonce = os.urandom(256)
    print("="*50)
    print("Cipher Key: {}".format(cipher.key))
    print("Nonce: {}".format(nonce))
    msg = "ChatGPT: The Kerckhoffs' Principle, formulated by Auguste Kerckhoffs in the 19th century, is a fundamental concept in cryptography that states that the security of a cryptographic system should not rely on the secrecy of the algorithm, but rather on the secrecy of the key. In other words, a cryptosystem should remain secure even if all the details of the encryption algorithm, except for the key, are publicly known. This principle emphasizes the importance of key management in ensuring the confidentiality and integrity of encrypted data and promotes the development of encryption algorithms that can be openly analyzed and tested by the cryptographic community, making them more robust and trustworthy."
    print("="*50)
    print("Plaintext: {}".format(msg))
    cipher.init_with_nonce(nonce)
    ct = cipher.encrypt(msg.encode())
    print("="*50)
    print("Ciphertext: {}".format(ct))
    cipher.init_with_nonce(nonce)
    dec = cipher.decrypt(ct)
    print("="*50)
    try:
        print("Decrypted: {}".format(dec))
        assert msg.encode() == dec
    except:
        print("Decryption failed")

    