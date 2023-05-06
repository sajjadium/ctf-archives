from typing import List
import os

sbox1 = [37, 9, 32, 12, 17, 41, 57, 47, 24, 36, 10, 44, 29, 18, 53, 38, 23, 14, 3, 61, 45, 62, 13, 46, 8, 5, 52, 63, 30, 4, 55, 28, 31, 11, 25, 0, 16, 35, 19, 22, 54, 59, 40, 42, 43, 6, 15, 33, 20, 50, 56, 26, 51, 34, 48, 49, 39, 27, 7, 1, 58, 60, 2, 21]
sbox2 = [4, 1, 51, 27, 53, 10, 57, 42, 55, 33, 41, 29, 52, 28, 24, 6, 40, 23, 36, 62, 3, 5, 16, 47, 63, 48, 58, 13, 31, 43, 39, 14, 56, 60, 2, 0, 26, 50, 38, 59, 21, 9, 35, 46, 8, 45, 54, 32, 18, 17, 15, 25, 11, 7, 12, 37, 20, 19, 34, 49, 44, 22, 30, 61]
sbox3 = [44, 13, 32, 0, 28, 61, 62, 48, 53, 60, 56, 18, 5, 36, 8, 41, 42, 22, 40, 35, 26, 59, 27, 54, 25, 37, 17, 31, 14, 34, 39, 47, 46, 15, 6, 2, 30, 63, 19, 52, 55, 11, 58, 50, 7, 38, 10, 43, 3, 9, 51, 4, 24, 57, 29, 23, 49, 16, 20, 21, 1, 33, 12, 45]
sbox4 = [57, 49, 51, 23, 53, 35, 39, 16, 17, 32, 50, 63, 8, 22, 19, 29, 59, 5, 31, 48, 44, 21, 28, 47, 25, 58, 61, 55, 20, 6, 62, 14, 54, 9, 37, 7, 11, 34, 43, 46, 3, 42, 2, 13, 10, 18, 45, 52, 0, 56, 41, 38, 26, 33, 30, 60, 36, 1, 12, 27, 40, 15, 24, 4]

pbox = [0, 12, 24, 30, 36, 42, 1, 6, 13, 18, 25, 37, 2, 7, 14, 26, 38, 43, 3, 15, 19, 27, 31, 39, 4, 8, 16, 20, 32, 44, 9, 17, 21, 28, 33, 45, 5, 10, 22, 34, 40, 46, 11, 23, 29, 35, 41, 47]

def invert_box(box):
    inv = [0 for _ in range(len(box))]
    for i in range(len(box)):
        inv[box[i]] = i
    return inv

def subs(values: List[int], sbox) -> List[int]:
    return [sbox[value] for value in values]

def subs2(values: List[int], sboxes) -> List[int]:
    return [(sboxes[i % len(sboxes)])[value] for i, value in enumerate(values)]

def permute(values: List[int], perm) -> List[int]:
    r = 0
    for v in values:
        r = (r << 6) | v
    p = 0
    for i in range(48):
        p |= ((r >> i) & 1) << perm[i]
    result = []
    for j in range(8):
        result.append(p & 0x3F)
        p >>= 6
    return result[::-1]

def xor(a: List[int], b: List[int]) -> List[int]:
    return [ai ^ bi for ai, bi in zip(a, b)]

def xorb(a : bytes, b : bytes) -> bytes:
    return bytes(xor(a, b))

def rotate(value : List[int]) -> List[int]:
    return value[2:] + value[:2]

def to_blocks(value: bytes) -> List[int]:
    value = int.from_bytes(value, "big")
    result = []
    for _ in range(8):
        result.append(value & 0x3F)
        value >>= 6
    return result[::-1]

def from_blocks(values: List[int]) -> bytes:
    r = 0
    for v in values:
        r = (r << 6) | v
    return r.to_bytes(6, "big")

def expand_key(key : bytes):
    W0 = to_blocks(key[:6])
    W1 = to_blocks(key[6:])
    W2 = xor(W0, subs(rotate(W1), sbox1))
    W3 = xor(W1, W2)
    W4 = xor(W2, subs(rotate(W3), sbox1))
    return W0, W1, W2, W3, W4


class LNRCipher:
    """LNR cipher object. Implements the LNR cipher, along with basic padding,
    ECB, and CBC encryption modes.

    LNR is a SPN-based block cipher that operates on 6-byte blocks. Despite the
    low number of rounds, our empirical tests show that LNR has security levels
    second-to-none, for more details see the whitepaper at: (TODO: Neil write
    this!)
    """
        
    def __init__(self, key):
        """Initializes a new cipher object with the given key.

        Parameters
        ----------
        key : bytes
            The 96-bit (12 byte) key used for this cipher object
        """
        round_keys = W0, W1, W2, W3, W4 = expand_key(key)
        sboxes = [sbox1, sbox2, sbox3, sbox4]
        self.enc_func = self._get_spn(sboxes=sboxes, pbox=pbox, round_keys=round_keys)

        ipbox = invert_box(pbox)
        self.dec_func = self._get_spn(sboxes=[invert_box(sbox) for sbox in sboxes], pbox=ipbox,
                        round_keys=(W4, permute(W3, ipbox), permute(W2, ipbox), permute(W1, ipbox), W0))

    def pad_message(self, message_bytes):
        """Pads the given message (bytes) to a multiple of 6 bytes long."""
        pad_value = 6 - (len(message_bytes) % 6)
        return message_bytes + pad_value * chr(pad_value).encode()

    def unpad_message(self, message_bytes):
        """Unpads the given message (bytes)."""
        assert len(message_bytes) >= 6
        pad_value = message_bytes[-1]
        assert 1 <= pad_value <= 6
        return message_bytes[:-pad_value]

    def encrypt_cbc(self, message_bytes):
        """Encrypts using the CBC mode of operation. IV is chosen randomly and
        prepended to the resulting ciphertext."""
        ciphertext_blocks = [os.urandom(6)] # initialize with IV
        for i in range(0, len(message_bytes), 6):
            message_block = message_bytes[i:i+6]
            ciphertext_blocks.append(self._encrypt_block(
                xorb(message_block, ciphertext_blocks[-1])))
        return b"".join(ciphertext_blocks)

    def decrypt_cbc(self, ciphertext_bytes):
        """Decrypts using the CBC mode of operation. Expects IV to be prepended
        to the ciphertext."""
        message_blocks = []
        for i in range(6, len(ciphertext_bytes), 6):
            last_ciphertext_block = ciphertext_bytes[i-6:i]
            ciphertext_block = ciphertext_bytes[i:i+6]
            message_blocks.append(xorb(self._decrypt_block(ciphertext_block),
                                       last_ciphertext_block))
        return b"".join(message_blocks)

    def encrypt_ecb(self, message_bytes):
        """Encrypts using the ECB mode of operation. This mode is not considered
        secure, and is only included for testing purposes."""
        return b''.join(self._encrypt_block(message_bytes[i:i+6]) for i in range(0,len(message_bytes),6))

    def decrypt_ecb(self, ciphertext_bytes):
        """Decrypts using the ECB mode of operation. This mode is not considered
        secure, and is only included for testing purposes."""
        return b''.join(self._decrypt_block(ciphertext_bytes[i:i+6]) for i in range(0,len(ciphertext_bytes),6))

    def _encrypt_block(self, byte_block):
        assert len(byte_block) == 6
        block = to_blocks(byte_block)
        block = self.enc_func(block)
        return from_blocks(block)

    def _decrypt_block(self, byte_block):
        assert len(byte_block) == 6
        block = to_blocks(byte_block)
        block = self.dec_func(block)
        return from_blocks(block)

    def _get_spn(self, sboxes, pbox, round_keys):
        K0, K1, K2, K3, K4 = round_keys
        
        def cipher(block):
            state = block
            state = xor(state, K0)
            state = subs2(state, sboxes)
            state = permute(state, pbox)
            
            state = xor(state, K1)
            state = subs2(state, sboxes)
            state = permute(state, pbox)
            
            state = xor(state, K2)
            state = subs2(state, sboxes)
            state = permute(state, pbox)
            
            state = xor(state, K3)
            state = subs2(state, sboxes)
            
            state = xor(state, K4)
            return state
        
        return cipher


if __name__ == "__main__":
    key = os.urandom(12)
    cipher = LNRCipher(key)

    def encrypt_file(filename):
        with open(filename, "rb") as f:
            file_bytes = f.read()
        encrypted_file_bytes = cipher.encrypt_cbc(cipher.pad_message(file_bytes))
        with open(filename + ".enc", "wb") as f:
            f.write(encrypted_file_bytes)

    encrypt_file("lol.bmp")
    encrypt_file("flag.txt")
