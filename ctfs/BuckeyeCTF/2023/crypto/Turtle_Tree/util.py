import secrets
import hashlib

empty_node_identifier = b"E"
leaf_node_identifier = b"L"


def bytes_to_bits(bs: bytes) -> list[int]:
    bits = [0] * (len(bs) * 8)
    for i in range(len(bits)):
        byte_index = i // 8
        bit_of_byte = i % 8
        bits[i] = int((bs[byte_index] << bit_of_byte) & (1 << 7) > 0)
    return bits


def bits_to_bytes(bits: list[int]) -> bytes:
    bs = [0] * ((len(bits) + 7) // 8)
    for i, x in enumerate(bits):
        if x == 1:
            byte_index = i // 8
            bit_of_byte = i % 8
            bs[byte_index] |= x << (7 - (bit_of_byte))
    return bytes(bs)


def get_nth_bit(bs: bytes, n: int) -> int:
    byte_index = n // 8
    bit_of_byte = n % 8
    return int((bs[byte_index] & (1 << (7 - bit_of_byte))) != 0)
