import random

# https://raw.githubusercontent.com/boppreh/aes/master/aes.py
import aes
from aes import AES


def inline_round(s, key):
    keym = aes.bytes2matrix(key)
    plain_state = aes.bytes2matrix(s)
    aes.sub_bytes(plain_state)
    aes.shift_rows(plain_state)
    aes.mix_columns(plain_state)
    aes.add_round_key(plain_state, keym)
    return aes.matrix2bytes(plain_state)


def main():
    print("Give me 256 unique plaintexts (hex encoded, 16 bytes long)")

    texts = []

    for i in range(256):
        texts.append(bytes.fromhex(input()))

    assert len(set(texts)) == 256
    assert all(len(c) == 16 for c in texts)

    target_texts = list(texts)
    random.shuffle(target_texts)

    print("Now give me a key such that:")
    for i in range(256):
        print(f"encrypt({texts[i].hex()}, key) == {target_texts[i].hex()}")

    print("TODO: key schedule is not implemented, sorry. Please just send me your round keys instead")
    # Originally I wanted to just use a normal AES encryption library, but with a sneaky bug that allows
    # user to skip key expansion if the provided key is long enough. This is not too crazy - for example this aes.py
    # would be *almost* vulnerable without "assert" in AES.__init__ and with n_rounds hardcoded to 14
    # In the end I decided against this, because:
    # - this chall is already hard enough without sneaky underhanded tricks
    # - last round weirdness makes the (intended) solution less elegant
    # So anyway there you have it - you can encrypt the data with any number of AES rounds, with round
    # keys completely under your control. Good luck.

    round_keys = []
    print("Give me your key (hex encoded)")
    key_data = bytes.fromhex(input())
    for i in range(0, len(key_data), 16):
        round_keys.append(key_data[i:i+16])

    assert all(len(c) == 16 for c in round_keys)

    for i, plaintext in enumerate(texts):
        for round_key in round_keys:
            plaintext = inline_round(plaintext, round_key)
        print(f"{plaintext.hex()} == {target_texts[i].hex()}")
        assert plaintext == target_texts[i]

    from flag import FLAG
    print("thx your flag is " + FLAG)


main()
