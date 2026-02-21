#!/usr/bin/env python3

from typing import List

IRREDUCIBLE_POLY = 0x11B

def gf_mult(a: int, b: int) -> int:
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        hi_bit = a & 0x80
        a = (a << 1) & 0xFF
        if hi_bit:
            a ^= (IRREDUCIBLE_POLY & 0xFF)
        b >>= 1
    return result

def gf_pow(base: int, exp: int) -> int:
    if exp == 0:
        return 1
    result = 1
    while exp > 0:
        if exp & 1:
            result = gf_mult(result, base)
        base = gf_mult(base, base)
        exp >>= 1
    return result

def gf_inv(a: int) -> int:
    if a == 0:
        return 0
    return gf_pow(a, 254)

def generate_sbox() -> List[int]:
    sbox = []
    for x in range(256):
        val = gf_pow(x, 23)
        val ^= 0x63
        sbox.append(val)
    return sbox

def generate_inv_sbox(sbox: List[int]) -> List[int]:
    inv_sbox = [0] * 256
    for i, v in enumerate(sbox):
        inv_sbox[v] = i
    return inv_sbox

SBOX = generate_sbox()
INV_SBOX = generate_inv_sbox(SBOX)

MIX_MATRIX = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

INV_MIX_MATRIX = [
    [0x0E, 0x0B, 0x0D, 0x09],
    [0x09, 0x0E, 0x0B, 0x0D],
    [0x0D, 0x09, 0x0E, 0x0B],
    [0x0B, 0x0D, 0x09, 0x0E]
]

RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def key_expansion(key: bytes, rounds: int = 6) -> List[bytes]:
    assert len(key) == 16
    words = []
    for i in range(4):
        words.append(list(key[4*i:4*i+4]))
    
    for i in range(4, 4 * (rounds + 1)):
        temp = words[i-1][:]
        if i % 4 == 0:
            temp = temp[1:] + temp[:1]
            temp = [SBOX[b] for b in temp]
            temp[0] ^= RCON[(i // 4) - 1]
        words.append([words[i-4][j] ^ temp[j] for j in range(4)])
    
    round_keys = []
    for r in range(rounds + 1):
        rk = bytes()
        for i in range(4):
            rk += bytes(words[r*4 + i])
        round_keys.append(rk)
    
    return round_keys

def sub_bytes(state: List[List[int]]) -> List[List[int]]:
    return [[SBOX[state[r][c]] for c in range(4)] for r in range(4)]

def inv_sub_bytes(state: List[List[int]]) -> List[List[int]]:
    return [[INV_SBOX[state[r][c]] for c in range(4)] for r in range(4)]

def shift_rows(state: List[List[int]]) -> List[List[int]]:
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][(c + r) % 4]
    return result

def inv_shift_rows(state: List[List[int]]) -> List[List[int]]:
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][(c - r) % 4]
    return result

def mix_columns(state: List[List[int]]) -> List[List[int]]:
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        for r in range(4):
            val = 0
            for i in range(4):
                val ^= gf_mult(MIX_MATRIX[r][i], state[i][c])
            result[r][c] = val
    return result

def inv_mix_columns(state: List[List[int]]) -> List[List[int]]:
    result = [[0]*4 for _ in range(4)]
    for c in range(4):
        for r in range(4):
            val = 0
            for i in range(4):
                val ^= gf_mult(INV_MIX_MATRIX[r][i], state[i][c])
            result[r][c] = val
    return result

def add_round_key(state: List[List[int]], round_key: bytes) -> List[List[int]]:
    result = [[0]*4 for _ in range(4)]
    for r in range(4):
        for c in range(4):
            result[r][c] = state[r][c] ^ round_key[r + 4*c]
    return result

def bytes_to_state(data: bytes) -> List[List[int]]:
    state = [[0]*4 for _ in range(4)]
    for i in range(16):
        state[i % 4][i // 4] = data[i]
    return state

def state_to_bytes(state: List[List[int]]) -> bytes:
    result = []
    for c in range(4):
        for r in range(4):
            result.append(state[r][c])
    return bytes(result)

class AES:
    ROUNDS = 4
    
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError
        self.key = key
        self.round_keys = key_expansion(key, self.ROUNDS)
    
    def encrypt(self, plaintext: bytes) -> bytes:
        if len(plaintext) != 16:
            raise ValueError
        
        state = bytes_to_state(plaintext)
        state = add_round_key(state, self.round_keys[0])
        
        for r in range(1, self.ROUNDS):
            state = sub_bytes(state)
            state = shift_rows(state)
            state = mix_columns(state)
            state = add_round_key(state, self.round_keys[r])
        
        state = sub_bytes(state)
        state = shift_rows(state)
        state = add_round_key(state, self.round_keys[self.ROUNDS])
        
        return state_to_bytes(state)
    
    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) != 16:
            raise ValueError
        
        state = bytes_to_state(ciphertext)
        state = add_round_key(state, self.round_keys[self.ROUNDS])
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        
        for r in range(self.ROUNDS - 1, 0, -1):
            state = add_round_key(state, self.round_keys[r])
            state = inv_mix_columns(state)
            state = inv_shift_rows(state)
            state = inv_sub_bytes(state)
        
        state = add_round_key(state, self.round_keys[0])
        return state_to_bytes(state)
