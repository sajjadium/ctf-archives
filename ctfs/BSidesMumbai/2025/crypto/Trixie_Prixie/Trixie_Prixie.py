import numpy as np
import base64
import sympy

def is_invertible_mod(matrix, mod):
    sym_mat = sympy.Matrix(matrix.tolist())
    try:
        _ = sym_mat.inv_mod(mod)
        return True
    except:
        return False

def generate_valid_matrix(mod=256, size=4):
    while True:
        mat = np.random.randint(0, 256, size=(size, size))
        if is_invertible_mod(mat, mod) and is_invertible_mod(np.rot90(mat), mod):
            return mat

def encrypt_message(message, key, block_size=4):
    message_bytes = [ord(c) for c in message]
    while len(message_bytes) % block_size != 0:
        message_bytes.append(0)
    encrypted = []
    for i in range(0, len(message_bytes), block_size):
        block = np.array(message_bytes[i:i+block_size])
        enc_block = key @ block % 256
        encrypted.extend(enc_block)
    return bytes(encrypted)

if __name__ == "__main__":
    flag = "BMCTF{REDACTED}"
    key = generate_valid_matrix()
    fake_key = np.rot90(key)
    cipher = encrypt_message(flag, key)
    cipher_b64 = base64.b64encode(cipher).decode()

    with open("cipher.txt", "w") as f:
        f.write(cipher_b64)

    np.save("key.npy", fake_key)
