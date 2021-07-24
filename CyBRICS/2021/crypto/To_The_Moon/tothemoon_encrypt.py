#!/usr/bin/python3.7
import hashlib
import os

from Crypto.Cipher import AES


NUM_REDUNDANT_BITS = 7


def pos_redundant_bits(data, r):
    # Place redundancy bits to the positions of the power of 2
    j = 0
    k = 1
    m = len(data)
    res = ''

    # Insert '0' to the positions of the power of 2
    for i in range(1, m + r + 1):
        if (i == 2 ** j):
            res = res + '0'
            j += 1
        else:
            res = res + data[-1 * k]
            k += 1

    return res[::-1]


def calc_parity_bits(arr, r):
    n = len(arr)

    # Searching for r parity bit
    for i in range(r):
        val = 0
        for j in range(1, n + 1):

            # If position has 1 in ith significant
            # position then Bitwise OR the array value
            # to find parity bit value.
            if (j & (2 ** i) == (2 ** i)):
                val = val ^ int(arr[-1 * j])
                # -1 * j is given since array is reversed

        # String Concatenation
        # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
        arr = arr[:n - (2 ** i)] + str(val) + arr[n - (2 ** i) + 1:]
    return arr


def calc_final_parity(arr):
    # Add a parity bit to the last bit of 128b string
    return "0" if arr.count("1") % 2 == 0 else "1"


def hamming_encode_block(block):
    bin_block = ''.join([bin(bt)[2:].zfill(8) for bt in block])
    arr = pos_redundant_bits(bin_block, NUM_REDUNDANT_BITS)
    arr = calc_parity_bits(arr, NUM_REDUNDANT_BITS)
    arr += calc_final_parity(arr)
    return arr


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 4:
        print("Usage: python tothemoon_encrypt.py <src filename> <dest filename> <password>")
        exit()

    flag = open(sys.argv[1], "rb").read()
    password = hashlib.md5(sys.argv[3].encode()).digest()
    iv = os.urandom(16)

    binary_blocks = []

    # Encode each 128b block with hamming 120/7 and add a parity bit
    while len(flag):
        current_block = flag[:15]
        if len(flag[15:]) == 0:
            current_block += b'\x00' * (15 - len(current_block) % 15)
        flag = flag[15:]

        binary_blocks.append(hamming_encode_block(current_block))

    binary_flag = "".join(binary_blocks)
    encoded_flag = bytes(int(binary_flag[i : i + 8], 2) for i in range(0, len(binary_flag), 8))

    encryptor = AES.new(password, AES.MODE_CBC, IV=iv)
    encrypted_flag = encryptor.encrypt(encoded_flag)
    secret_data = iv + encrypted_flag

    with open(sys.argv[2], "wb") as w:
        w.write(secret_data)
