from sage.all import *
import secrets
import os


BLOCK_LEN = 8
SECRETS = 30


def create_sbox():
    sbox = [i for i in range(256)]
    for i in range(256 - 1, -1, -1):
        U = secrets.randbelow(i + 1)
        sbox[i], sbox[U] = sbox[U], sbox[i]
    return sbox


def create_sbox_layer(sz):
    return [create_sbox() for _ in range(sz)]


def create_linear(sz):
    while True:
        M = []
        for i in range(sz * 8):
            R = secrets.randbits(sz * 8)
            M.append([])
            for j in range(sz * 8):
                M[i].append((R >> j) & 1)
        M = Matrix(GF(2), M)
        if M.det() == 1:
            break
    return M


def apply_sbox(inpt, sboxlist):
    answer = b""
    for (a, b) in zip(inpt, sboxlist):
        answer += bytes([b[a]])
    return answer


def bitify(inpt):
    ans = []
    for c in inpt:
        for i in range(8):
            ans.append((c >> i) & 1)
    return vector(GF(2), ans)


def unbitify(inpt):
    ans = []
    for i in range(0, len(inpt), 8):
        c = 0
        for j in range(8):
            c += pow(2, j) * int(inpt[j + i])
        ans.append(c)
    return bytes(ans)


def apply_linear(inpt, layer):
    return unbitify(bitify(inpt) * layer)


def genkey(num_layers, start_layer):
    LAYERS = []
    for i in range(num_layers):
        if i % 2 == start_layer:
            LAYERS.append(['sbox', create_sbox_layer(BLOCK_LEN)])
        else:
            LAYERS.append(['linear', create_linear(BLOCK_LEN)])
    return LAYERS


def encrypt_block(pt, key):
    ct = pt
    for a in key:
        if a[0] == 'sbox':
            ct = apply_sbox(ct, a[1])
        else:
            ct = apply_linear(ct, a[1])
    return ct


def main():
    key = genkey(3, 0)

    while True:
        pt = input("Insert plaintext \n> ")
        if pt == "-1":
            break
        try:
            pt = bytes.fromhex(pt)
            assert (len(pt) == BLOCK_LEN)
        except:
            print("An error occured")
            exit(0)
        ct = encrypt_block(pt, key)
        print("Ciphertext :", ct.hex())

    for i in range(SECRETS):
        print(f"SECRET {i + 1}/{SECRETS}")
        secret = os.urandom(BLOCK_LEN)
        enc = encrypt_block(secret, key)
        print("Encrypted secret:", enc.hex())

        pt = input("What is the secret? \n> ")
        try:
            pt = bytes.fromhex(pt)
            assert (len(pt) == BLOCK_LEN)
        except:
            print("An error occured")
            exit(0)
        if pt != secret:
            print(f"Incorrect secret. Secret was: {secret.hex()}")
            exit(0)

    print("Congratulations! You guessed all secrets. Here is your flag:")
    print(open("flag.txt").read())


if __name__ == '__main__':
    main()
