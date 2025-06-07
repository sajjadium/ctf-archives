import random
from random import randint
import sys
from Crypto.Util import number
import hashlib 

def encrypt_outer(plaintext_ords, key):
    cipher = []
    key_offset = key % 256
    for val in plaintext_ords:
        if not isinstance(val, int):
            raise TypeError
        cipher.append((val + key_offset) * key)
    return cipher

def dynamic_xor_encrypt(plaintext_bytes, text_key_bytes):
    encrypted_ords = []
    key_length = len(text_key_bytes)
    if not isinstance(plaintext_bytes, bytes):
        raise TypeError
    for i, byte_val in enumerate(plaintext_bytes[::-1]):
        key_byte = text_key_bytes[i % key_length]
        encrypted_ords.append(byte_val ^ key_byte)
    return encrypted_ords

def generate_dh_key():
    p = number.getPrime(1024)
    g = number.getPrime(1024)
    a = randint(p - 10, p)
    b = randint(g - 10, g)
    u = pow(g, a, p)
    v = pow(g, b, p)
    key = pow(v, a, p)
    b_key = pow(u, b, p)
    if key != b_key:
        sys.exit(1)
    return p, g, u, v, key

def generate_challenge_files(flag_file="flag.txt", params_out="params.txt", enc_flag_out="enc_flag"):
    try:
        with open(flag_file, "r") as f:
            flag_plaintext = f.read().strip()
    except FileNotFoundError:
        sys.exit(1)
    flag_bytes = flag_plaintext.encode('utf-8')
    p, g, u, v, shared_key = generate_dh_key()
    xor_key_str = hashlib.sha256(str(shared_key).encode()).hexdigest()
    xor_key_bytes = xor_key_str.encode('utf-8')
    intermediate_ords = dynamic_xor_encrypt(flag_bytes, xor_key_bytes)
    final_cipher = encrypt_outer(intermediate_ords, shared_key)
    with open(params_out, "w") as f:
        f.write(f"p = {p}\n")
        f.write(f"g = {g}\n")
        f.write(f"u = {u}\n")
        f.write(f"v = {v}\n")
    with open(enc_flag_out, "w") as f:
        f.write(str(final_cipher))

if __name__ == "__main__":
    try:
        with open("flag.txt", "x") as f:
            f.write("tjctf{d3f4ult_fl4g_f0r_t3st1ng}")
    except FileExistsError:
        pass
    generate_challenge_files()
