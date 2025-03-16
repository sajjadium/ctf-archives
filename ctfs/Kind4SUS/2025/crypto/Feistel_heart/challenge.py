from Crypto.Util.number import bytes_to_long, getPrime, long_to_bytes
from Crypto.Util.Padding import pad
import os, signal

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("KSUS{") and FLAG.endswith("}"))

def xor_bytes(bytes_a, bytes_b):
    return bytes(a ^ b for a, b in zip(bytes_a, bytes_b)).ljust(2, b'\x00')

def f(sub_block, round_key, modulus):
    return long_to_bytes((bytes_to_long(sub_block) + pow(65537, bytes_to_long(round_key), modulus)) % (1<<17-1)).ljust(2, b'\x00')

def encrypt_block(block, key, modulus, rounds=8, shortcut=False):
    sub_block_1 = block[:2].ljust(2, b'\x00')
    sub_block_2 = block[2:4].ljust(2, b'\x00')
    sub_block_3 = block[4:].ljust(2, b'\x00')
    for i in range(0, rounds):
        round_key = key[i*2:i*2+2]
        new_sub_block_1 = xor_bytes(sub_block_1, sub_block_2) 
        new_sub_block_2 = f(sub_block_3, round_key, modulus)
        new_sub_block_3 = xor_bytes(sub_block_2, round_key)
        sub_block_1 = new_sub_block_1
        sub_block_2 = new_sub_block_2
        sub_block_3 = new_sub_block_3
        if shortcut and sub_block_1 == b"\xff\xff":
            break
    return sub_block_1 + sub_block_2 + sub_block_3

def encrypt(plaintext, key, modulus):
    iv = os.urandom(6)
    padded = pad(plaintext.encode(), 6)
    blocks = [padded[i:i+6] for i in range(0, len(padded), 6)] 
    res = []
    for i in range(len(blocks)):
        if i == 0: block = xor_bytes(blocks[i], iv)
        else: block = xor_bytes(blocks[i], bytes.fromhex(res[-1]))
        res.append(encrypt_block(block, key, modulus).hex())
    return iv.hex() + "".join(res)

def handle():
    key = os.urandom(16)
    N = getPrime(1024)
    print("flag =", encrypt(FLAG, key, N))
    print("N =", N)

    encrypted = []
    while True:
        print("[1] Encrypt")
        print("[2] Exit")
        opt = input("> ")
        
        if opt == "1":
            plaintext = input("Enter your fantastic plaintext (in hex): ")
            if len(plaintext) % 2 != 0 or len(plaintext) < 2 or len(plaintext) > 12:
                print("It doesn't look fine to me :/")
            elif plaintext in encrypted:
                print("Nah, you've already encrypted it!")
            else:
                encrypted.append(plaintext)
                ciphertext = encrypt_block(bytes.fromhex(plaintext).rjust(6, b"\x00"), key, N, shortcut=True)
                print("Here it is: " + ciphertext.hex())
        elif opt == "2":
            print("Bye (^-^)")
            exit(0)
        else:
            print("Nope :/")

if __name__ == "__main__":
    signal.alarm(300)
    handle()