# note that all of this info is diff on the challenge server :)

FLAG = 'f{hi_bob}}'
key = 7
ws = ['bad stuff']


def encrypt(text: str, key: int):
    result = ''

    for c in text:
        if c.isupper():
            c_index = ord(c) - ord('A')
            c_shifted = (c_index + key) % 26 + ord('A')
            result += chr(c_shifted)
        elif c.islower():
            c_index = ord(c) - ord('a')
            c_shifted = (c_index + key) % 26 + ord('a')
            result += chr(c_shifted)
        elif c.isdigit():
            c_new = (int(c) + key) % 10
            result += str(c_new)
        else:
            result += c

    return result


flag_enc = encrypt(FLAG, key)
