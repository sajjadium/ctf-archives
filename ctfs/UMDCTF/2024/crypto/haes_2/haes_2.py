#!/usr/local/bin/python
# adapted from https://github.com/boppreh/aes/blob/master/aes.py, 
# which is in turn adapted from https://github.com/bozhu/AES-Python
# LICENSE:
'''
Copyright (C) 2012 Bo Zhu http://about.bozhu.me

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
'''

import os

N_ROUNDS = 4 # NOTE THAT THIS IS DIFFERENT FROM THE OTHER CHALLENGE

def expand_key(master_key):
    """
    Expands and returns a list of key matrices for the given master_key.
    """

    # Round constants https://en.wikipedia.org/wiki/AES_key_schedule#Round_constants
    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
        0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
        0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
        0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
    )

    # Initialize round keys with raw key material.
    key_columns = [list(master_key[4*i:4*i+4]) for i in range(16)]

    iteration_size = len(master_key) // 4

    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 16:
        # Copy previous word.
        word = key_columns[-1].copy()
        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift
            word.append(word.pop(0))
            # Map to S-BOX.
            word = [s_box[b] for b in word]
            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            word[0] ^= r_con[i]
            i += 1

        # XOR with equivalent word from previous iteration.
        word = [i^j for i, j in zip(word, key_columns[-iteration_size])]
        key_columns.append(word)

    full_key_stream = [ kb for key_column in key_columns for kb in key_column ]
    return [full_key_stream[i*64:(i+1)*64] for i in range(0,N_ROUNDS + 1, 1)]

def bytes_to_state(text):
    return [ [ [text[i+j+k] for k in range(4) ] for j in range(0, 16, 4) ] for i in range(0, 64, 16)]

def state_to_bytes(state):
    arr = [0] * 64

    for i in range(4):
        for j in range(4):
            for k in range(4):
                arr[16*i+4*j+k] = state[i][j][k]

    return bytes(arr)


def add_round_key(s, rk):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state[i][j][k] = s[i][j][k] ^ rk[16*i+4*j+k]

    return new_state

s_box = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
]

inv_s_box = [s_box.index(i) for i in range(256)]

def sub_bytes(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state[i][j][k] = s_box[s[i][j][k]]

    return new_state


# provided for convenience
def inv_sub_bytes(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state[i][j][k] = inv_s_box[s[i][j][k]]

    return new_state

def shift_planes(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state[(i+j) % 4][(j+k) % 4][k] = s[i][j][k]
    return new_state

# provided for convenience
def inv_shift_planes(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                new_state[i][j][k] = s[(i+j)%4][(j+k)%4][k]
    return new_state

xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    b = [x for x in a] # copy
    u = a[0]
    b[0] ^= t ^ xtime(a[0] ^ a[1])
    b[1] ^= t ^ xtime(a[1] ^ a[2])
    b[2] ^= t ^ xtime(a[2] ^ a[3])
    b[3] ^= t ^ xtime(a[3] ^ u)
    return b


def mix_columns(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    for i in range(4):
        for j in range(4):
            new_state[i][j] = mix_single_column(s[i][j])
    return new_state

# provided for convenience
def inv_mix_columns(s):
    new_state = [[[0 for _ in range(4)] for _ in range(4)] for _ in range(4)]

    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        for j in range(4):
            u = xtime(xtime(s[i][j][0] ^ s[i][j][2]))
            v = xtime(xtime(s[i][j][1] ^ s[i][j][3]))
            new_state[i][j][0] = s[i][j][0] ^ u
            new_state[i][j][1] = s[i][j][1] ^ v
            new_state[i][j][2] = s[i][j][2] ^ u
            new_state[i][j][3] = s[i][j][3] ^ v

    return mix_columns(new_state)

def encrypt(key, plaintext):
    assert(len(key) == 64)
    assert(len(plaintext) == 64)
    round_keys = expand_key(key)

    state = bytes_to_state(plaintext)

    state = add_round_key(state, round_keys[0])

    for i in range(1, N_ROUNDS):
        state = sub_bytes(state)
        state = shift_planes(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])


    state = sub_bytes(state)
    state = shift_planes(state)
    state = add_round_key(state, round_keys[N_ROUNDS])

    return state_to_bytes(state)



if __name__ == "__main__":
    key = os.urandom(64)

    flag = open("flag.txt", "rb").read()
    flag += b'\x00' * (64 - len(flag))

    print("Encrypted Flag: ", bytes.hex(encrypt(key, flag)))

    print("The Baron has gotten tired of your long and meaningless messages.")
    print("Be very careful about what you say.")
    print("Leave your message for Baron Harkonnen here: ")
    pt = input()
    if not pt.isprintable():
        print("What is this meaningless garbage???")
        exit()
    pt = pt.encode()
    if len(pt) % 64 != 0:
        print("Must be a multiple of block size.")
        exit()
    elif (len(pt) // 64) > 3:
        print("Too long.")
        exit()
    print("Encrypted message:")
    i = 0 
    while i < len(pt):
        print(bytes.hex(encrypt(key, pt[i:i+64])), end='')
        i += 64
    
    print()
    print("Your message has been sent to the Baron.")
