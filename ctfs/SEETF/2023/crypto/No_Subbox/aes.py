# Modified from https://github.com/boppreh/aes/blob/master/aes.py

from element import Element

RCON = [*map(Element, (
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
))]
N_ROUNDS = 6
N_BYTES = 16


def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] += k[i][j]


def mix_single_column(a):
    b1, b2, b3, b4 = (
        2*a[0] + 3*a[1] + 1*a[2] + 1*a[3],
        1*a[0] + 2*a[1] + 3*a[2] + 1*a[3],
        1*a[0] + 1*a[1] + 2*a[2] + 3*a[3],
        3*a[0] + 1*a[1] + 1*a[2] + 2*a[3]
    )
    a[0], a[1], a[2], a[3] = b1, b2, b3, b4


def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])


def xor_bytes(a, b):
    return [i+j for i, j in zip(a, b)]


def bytes2matrix(text):
    return [[*map(Element, text[i:i+4])] for i in range(0, len(text), 4)]


def matrix2bytes(matrix):
    return bytes(map(lambda m: m.to_byte(), sum(matrix, [])))


def expand_key(master_key):

    key_columns = bytes2matrix(master_key)
    iteration_size = len(master_key) // 4

    i = 1
    while len(key_columns) < (N_ROUNDS + 1) * 4:
        # Copy previous word.
        word = list(key_columns[-1])

        # Perform schedule_core once every "row".
        if len(key_columns) % iteration_size == 0:
            # Circular shift.
            word.append(word.pop(0))
            # XOR with first byte of R-CON, since the others bytes of R-CON are 0.
            word[0] += RCON[i]
            i += 1

        # XOR with equivalent word from previous iteration.
        word = xor_bytes(word, key_columns[-iteration_size])
        key_columns.append(word)

    # Group key words in 4x4 byte matrices.
    return [key_columns[4*i: 4*(i+1)] for i in range(len(key_columns) // 4)]


def encrypt_block(key, plaintext):

    assert len(plaintext) == N_BYTES

    plain_state = bytes2matrix(plaintext)
    round_keys = expand_key(key)

    add_round_key(plain_state, round_keys[0])

    for i in range(1, N_ROUNDS):
        shift_rows(plain_state)
        mix_columns(plain_state)
        add_round_key(plain_state, round_keys[i])

    shift_rows(plain_state)
    add_round_key(plain_state, round_keys[-1])

    return matrix2bytes(plain_state)
