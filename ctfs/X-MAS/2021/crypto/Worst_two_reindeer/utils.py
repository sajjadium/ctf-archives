def bytes_2_bit_array(x):
    result = []
    for b in x:
        result += [int(a) for a in bin(b)[2:].zfill(8)]
    return result


def bit_array_2_bytes(x):
    result = b''
    for i in range(0, len(x), 8):
        result += int(''.join([chr(a + ord('0')) for a in x[i: i + 8]]), 2).to_bytes(1, byteorder='big')
    return result


def xor(a, b):
    return [x ^ y for x, y in zip(a, b)]


def rotate_right(arr, shift):
    return arr[-shift:] + arr[:-shift]


def rotate_left(arr, shift):
    return arr[shift:] + arr[:shift]
