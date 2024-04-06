from Crypto.Random import get_random_bytes

KEY_LEN = 100
key = get_random_bytes(KEY_LEN)
R = 0x01


def RGEN():
    global R
    R = ((R << 1) ^ (0x71 if (R & 0x80) else 0)) & 0xFF
    return R


def xor_text(text, key):
    return bytes([text[i] ^ key[i] for i in range(len(text))])


def next_key(key):
    return bytes([key[i] ^ RGEN() for i in range(len(key))])


def encrypt(text, key):
    ciphertext = b""

    blocks = [text[i : i + KEY_LEN] for i in range(0, len(text), KEY_LEN)]

    for block in blocks:
        ciphertext += xor_text(block, key)
        key = next_key(key)

    return ciphertext


# ---

text = b""
with open("text.txt", "rb") as f:
    text = f.read()

ciphertext = encrypt(text, key)
with open("../res/ciphertext.txt", "wb") as g:
    g.write(ciphertext)
