import os


def xnor_bit(a_bit, b_bit):
    if a_bit == "1" and b_bit == "1":
        return "1"
    elif a_bit == "1" and b_bit == "0":
        return "0"
    elif a_bit == "0" and b_bit == "1":
        return "0"
    elif a_bit == "0" and b_bit == "0":
        return "1"


def xnor_byte(a_byte, b_byte):
    a_bits = get_bits_from_byte(a_byte)
    b_bits = get_bits_from_byte(b_byte)

    result_bits = [xnor_bit(a_bits[i], b_bits[i]) for i in range(8)]
    result_byte = get_byte_from_bits(result_bits)
    return result_byte


def xnor_bytes(a_bytes, b_bytes):
    assert len(a_bytes) == len(b_bytes)

    return bytes([xnor_byte(a_bytes[i], b_bytes[i]) for i in range(len(a_bytes))])


def get_bits_from_byte(byte):
    return list("{:08b}".format(byte))


def get_byte_from_bits(bits):
    return int("".join(bits), 2)


message = b"Blue is greener than purple for sure!"
key = os.urandom(37)

flag = b"bctf{???????????????????????????????}"


def main():
    print(f"Key: {key.hex()}")
    print(f"\nMessage: {message}")

    encrypted = xnor_bytes(message, key)
    print(f"Enrypted message: {encrypted.hex()}")

    print(f"\nFlag: {flag}")
    encrypted_flag = xnor_bytes(flag, key)
    print(f"Encrypted flag: {encrypted_flag.hex()}")


if __name__ == "__main__":
    main()
