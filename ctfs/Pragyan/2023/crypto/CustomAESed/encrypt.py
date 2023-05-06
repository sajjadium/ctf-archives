from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from pwn import xor
from hashlib import sha256
from base64 import b64encode


def encryption(text, key, iv):
    assert len(iv) == 12
    block_size = AES.block_size
    text = pad(text, block_size)
    encrypted = bytes()
    cipher = AES.new(key, AES.MODE_ECB)
    for n in range(1, (len(text) // block_size) + 1):
        num = bytes.fromhex("{0:08x}".format(n))
        pt = iv[:8] + num + iv[8:]
        ct = cipher.encrypt(pt)
        encrypted += xor(text[(n - 1) * block_size: n * block_size], ct)
    return encrypted


def data_encoder(text):
    bin_text = bin(bytes_to_long(text))[2:]
    encoded_text = []
    parity_bits = 0
    x = 1
    y = 0
    while y < len(bin_text):
        if x & (x - 1) == 0:
            encoded_text.append('0')
            parity_bits += 1
        else:
            encoded_text.append(bin_text[y])
            y += 1
        x += 1
    for x in range(parity_bits):
        pos_bit = 0
        for bit in range(1, len(encoded_text) + 1):
            if bit & (2 ** x):
                pos_bit ^= int(encoded_text[bit - 1])
        encoded_text[(2 ** x) - 1] = str(pos_bit)
    return ("".join(encoded_text)).encode()


pt = r"--REDACTED--"
text = data_encoder(pt.encode())
print(text.hex())

key = sha256("128bit_secretkey".encode()).digest()
iv = bytes.fromhex("1670dc9a0ed463028e1a7d68")
ct = encryption(text, key, iv)
ct = iv + ct
print(f"ct = {b64encode(ct).decode()}")

# ct = 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
