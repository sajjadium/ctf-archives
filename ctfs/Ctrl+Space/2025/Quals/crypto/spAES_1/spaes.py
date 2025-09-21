from Crypto.Util.Padding import pad, unpad

SBOX = [4, 14, 13, 5, 0, 9, 2, 15, 11, 8, 12, 3, 1, 6, 7, 10]

ROUNDS = 6

CONSTS = ['6d6ab780eb885a101263a3e2f73520c9', 'f71df57947881932a33a3a0b8732b912', '0aa5df6fadf91c843977d378cc721147', '4a8f29cf09b62619c596465a59fb9827', '29b408cfd4910c80866f5121c6b1cc77', '8589c67a30dbced873b34bd04f40b7cb', '6d64bc8485817ba330fc81b9d2899532', '46495adad2786761ae89e8c26ff1c769', '747470d62b219d12abf9a0816b950639', '4ed2d429061e5d13a2b2ad1df1e63110']

def rotr_128(x, n):
    return ((x >> n) | (x << (128 - n))) & ((1 << 128) - 1)

def rotl_4(x, n):
    return ((x << n) | (x >> (4 - n))) & ((1 << 4) - 1)

def to_matrix(bts):
    return [
        [bts[i] >> 4 for i in range(0, 16, 2)],
        [bts[i] & 0x0F for i in range(0, 16, 2)],
        [bts[i] >> 4 for i in range(1, 16, 2)],
        [bts[i] & 0x0F for i in range(1, 16, 2)],
    ]

def from_matrix(state):
    return bytes([state[i][j] << 4 | state[i + 1][j] for j in range(8) for i in (0, 2)])

def shift_rows(state):
    return [
        state[0],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3]
    ]

def mix_columns(state):
    mixed = [[0 for i in range(8)] for j in range(4)]
    for i in range(8):
        mixed[0][i] = state[1][i] ^ rotl_4(state[2][i], 1) ^ rotl_4(state[3][i], 2)
        mixed[1][i] = state[2][i] ^ rotl_4(state[3][i], 1) ^ rotl_4(state[0][i], 2)
        mixed[2][i] = state[3][i] ^ rotl_4(state[0][i], 1) ^ rotl_4(state[1][i], 2)
        mixed[3][i] = state[0][i] ^ rotl_4(state[1][i], 1) ^ rotl_4(state[2][i], 2)
    return mixed

def enc(m, k, t):
    assert len(m) == 16
    assert len(k) == 16
    assert len(t) == 16

    RCON = [bytes.fromhex(x) for x in CONSTS]

    final_key = int.from_bytes(k, byteorder='big')
    final_key = rotr_128(final_key, 63) ^ (final_key >> 1)
    final_key = int.to_bytes(final_key, length=16, byteorder='big')
    
    state = to_matrix(m)
    key_matrix = to_matrix(k)
    tweak_matrix = to_matrix(t)
    final_key_matrix = to_matrix(final_key)

    state = [[state[i][j] ^ key_matrix[i][j] for j in range(8)] for i in range(4)]

    for r in range(ROUNDS-1):
        state = [[SBOX[state[i][j]] for j in range(8)] for i in range(4)]
        state = shift_rows(state)
        state = mix_columns(state)
        round_const_matrix = to_matrix(RCON[r])
        state = [[state[i][j] ^ round_const_matrix[i][j] for j in range(8)] for i in range(4)]

        if r % 2 == 0:
            state = [[state[i][j] ^ key_matrix[i][j] for j in range(8)] for i in range(4)]
        else:
            state = [[state[i][j] ^ tweak_matrix[i][j] for j in range(8)] for i in range(4)]

    state = [[SBOX[state[i][j]] for j in range(8)] for i in range(4)]
    state = shift_rows(state)
    state = [[state[i][j] ^ final_key_matrix[i][j] for j in range(8)] for i in range(4)]

    c = from_matrix(state)
    return c

class spAES:
    def __init__(self, master_key):
        self.master_key = master_key
        self.tweak = b"\x00"*16

    def encrypt_ecb(self, plaintext):
        plaintext = pad(plaintext, 16)
        blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
        return b"".join([enc(block, self.master_key, self.tweak) for block in blocks])
