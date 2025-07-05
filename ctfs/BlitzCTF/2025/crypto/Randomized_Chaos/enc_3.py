import random

flag = b"Blitz{REDACTED}"

def complex_encrypt(flag_bytes, key_bytes):
    result = bytearray()
    for i in range(len(flag_bytes)):
        k = key_bytes[i] % 256
        f = flag_bytes[i]
        r = ((f ^ k) & ((~k | f) & 0xFF))
        r = ((r << (k % 8)) | (r >> (8 - (k % 8)))) & 0xFF
        result.append(r)
    return result

with open("output.txt", "w") as f:
    for _ in range(624 * 10):
        key = [random.getrandbits(32) for _ in range(len(flag))]
        ct = complex_encrypt(flag, key)
        f.write(ct.hex() + '\n')