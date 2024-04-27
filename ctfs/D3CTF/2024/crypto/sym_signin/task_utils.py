import hashlib
import struct
S = [0xc, 0x5, 0x6, 0xb, 0x9, 0x0, 0xa, 0xd,
     0x3, 0xe, 0xf, 0x8, 0x4, 0x7, 0x1, 0x2]

P = [0, 8, 16, 24, 1, 9, 17, 25, 2, 10, 18, 26, 3, 11, 19, 27,
     4, 12, 20, 28, 5, 13, 21, 29, 6, 14, 22, 30, 7, 15, 23, 31]


def S_16bit(x: int) -> int:
    result = 0
    for i in range(4):
        block = (x >> (i * 4)) & 0xF
        sbox_result = S[block]
        result |= sbox_result << (i * 4)
    return result


def S_layer(x: int) -> int:
    return (S_16bit(x >> 16) << 16) | S_16bit(x & 0xffff)


def P_32bit(x: int) -> int:
    binary_result = format(x, '032b')
    permuted_binary = ''.join(binary_result[i] for i in P)
    result = int(permuted_binary, 2)
    return result


def key_schedule(key):
    return ((key << 31 & 0xffffffff) + (key << 30 & 0xffffffff) + key) & 0xffffffff


def enc_round(message: int, key: int) -> int:
    result = message ^ key
    result = S_layer(result)
    result = P_32bit(result)
    return result


def encrypt(message: int, key: int, ROUND: int) -> int:
    ciphertext = message
    for _ in range(ROUND):
        ciphertext = enc_round(ciphertext, key)
        key = key_schedule(key)

    ciphertext = S_layer(ciphertext)
    ciphertext ^= key

    return ciphertext


def key_ex(num: int) -> int:
    result = 0
    bit_position = 0
    while num > 0:
        original_bits = num & 0b111
        parity_bit = bin(original_bits).count('1') % 2
        result |= (original_bits << (bit_position + 1)
                   ) | (parity_bit << bit_position)
        num >>= 3
        bit_position += 4
    return result


def write_to_binary_file(uint32_list, output_file):
    with open(output_file, 'wb') as f:
        for number in uint32_list:
            # Pack the integer as an unsigned 32-bit integer (using 'I' format)
            packed_data = struct.pack('<I', number)
            f.write(packed_data)


def read_from_binary_file(input_file):
    uint32_list = []
    with open(input_file, 'rb') as f:
        while True:
            # Read 4 bytes (32 bits) from the file
            data = f.read(4)
            if not data:
                break  # End of file reached
            number = struct.unpack('<I', data)[0]
            uint32_list.append(number)

    return uint32_list


def bytes_to_uint32_list(byte_string, fill_value=None):
    uint32_list = []

    remainder = len(byte_string) % 4
    if remainder != 0:
        padding_bytes = 4 - remainder
        if fill_value is not None:
            byte_string += bytes([fill_value] * padding_bytes)

    for i in range(0, len(byte_string), 4):
        data_chunk = byte_string[i:i+4]
        number = struct.unpack('<I', data_chunk)[0]
        uint32_list.append(number)

    return uint32_list


def l6shad(x):
    # Convert the 24-bit integer x to a bytes object (3 bytes)
    x_bytes = x.to_bytes(3, 'big')
    sha256_hash = hashlib.sha256(x_bytes).hexdigest()
    last_six_hex_digits = sha256_hash[-6:]
    result_int = int(last_six_hex_digits, 16)

    return result_int
