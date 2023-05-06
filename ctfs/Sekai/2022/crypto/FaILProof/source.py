import hashlib
from os import urandom
from flag import FLAG


def gen_pubkey(secret: bytes, hasher=hashlib.sha512) -> list:
    def hash(m): return hasher(m).digest()
    state = hash(secret)
    pubkey = []
    for _ in range(len(hash(b'0')) * 4):
        pubkey.append(int.from_bytes(state, 'big'))
        state = hash(state)
    return pubkey


def happiness(x: int) -> int:
    return x - sum((x >> i) for i in range(1, x.bit_length()))


def encode_message(message: bytes, segment_len: int) -> list:
    message += bytes(segment_len - len(message) % (segment_len))
    encoded = []
    for i in range(0, len(message), segment_len):
        block = message[i:i + segment_len]
        encoded.append(int.from_bytes(block, 'big'))
    return encoded


def encrypt(pubkey: list, message: bytes) -> list:
    encrypted_blocks = []
    for block_int in encode_message(message, len(pubkey) // 4):
        encrypted_blocks.append([happiness(i & block_int) for i in pubkey])
    return encrypted_blocks


secret = urandom(16)
A = gen_pubkey(secret, hashlib.sha256)
enc = encrypt(A, FLAG)
print(secret.hex())
print(enc)
