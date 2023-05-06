#!/usr/bin/env python3

import signal
import os

ROUNDS = 2**22 + 2
QUERIES = 500

sbox = [109, 86, 136, 240, 199, 237, 30, 94, 134, 162, 49, 78, 111, 172, 214, 117, 90, 226, 171, 105, 248, 216, 48, 196, 130, 203, 179, 223, 12, 123, 228, 96, 225, 113, 168, 5, 208, 124, 146, 184, 206, 77, 72, 155, 191, 83, 142, 197, 144, 218, 255, 39, 236, 221, 251, 102, 207, 57, 15, 159, 98, 80, 145, 22, 235, 63, 125, 120, 245, 198, 10, 233, 56, 92, 99, 55, 187, 43, 25, 210, 153, 101, 44, 252, 93, 82, 182, 9, 36, 247, 129, 3, 84, 74, 128, 69, 20, 246, 141, 2, 41, 169, 59, 217, 137, 95, 189, 138, 116, 7, 180, 60, 18, 238, 73, 133, 121, 62, 87, 40, 213, 37, 33, 122, 200, 192, 118, 205, 135, 53, 58, 89, 201, 21, 193, 149, 8, 112, 81, 243, 131, 158, 188, 154, 211, 147, 164, 195, 181, 222, 178, 67, 76, 115, 150, 127, 103, 254, 1, 249, 186, 88, 177, 61, 14, 152, 106, 161, 229, 70, 160, 175, 29, 224, 66, 38, 91, 79, 185, 114, 190, 6, 110, 194, 250, 119, 0, 230, 176, 51, 104, 219, 215, 151, 75, 13, 23, 165, 11, 139, 42, 167, 52, 85, 156, 253, 163, 19, 35, 140, 107, 31, 143, 166, 32, 47, 132, 239, 234, 71, 241, 157, 170, 64, 100, 16, 97, 227, 204, 34, 4, 50, 126, 209, 174, 46, 45, 28, 232, 24, 212, 244, 220, 173, 17, 54, 231, 108, 65, 202, 27, 68, 26, 183, 148, 242]

def encrypt1(k, plaintext):
    a,b,c,d = plaintext
    for i in range(ROUNDS):
        a ^= sbox[b ^ k[(2*i)&3]]
        c ^= sbox[d ^ k[(2*i+1)&3]]
        a,b,c,d = b,c,d,a
    return bytes([a,b,c,d])

def encrypt2(k, plaintext):
    a,b,c,d = plaintext
    for i in range(ROUNDS)[::-1]:
        b,c,d,a = a,b,c,d
        c ^= sbox[d ^ k[(2*i)&3]]
        a ^= sbox[b ^ k[(2*i+1)&3]]
    return bytes([a,b,c,d])

key = os.urandom(4)
result = b""

def handle_queries(f):
    global result
    num_queries = 0
    while True:
        query = bytes.fromhex(input("input (hex): "))
        assert len(query) % 4 == 0
        assert len(query) > 0
        for i in range(0, len(query), 4):
            result += f(key, query[i:i+4])
            num_queries += 1
            if num_queries >= QUERIES:
                return

print("ENCRYPT 1")
handle_queries(encrypt1)

print("ENCRYPT 2")
handle_queries(encrypt2)

print("result:", result.hex())
signal.alarm(30)

guess = bytes.fromhex(input("key guess (hex): "))
if guess == key:
    print("Congrats!")
    with open("flag", "r") as f:
        print(f.read().strip())
else:
    print("Wrong key.")
    print("Expected:", key.hex())
