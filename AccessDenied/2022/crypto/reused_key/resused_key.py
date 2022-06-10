import os

flag = "XXXX"
some_simple_text = "YYYY"
key = os.urandom(43)

def encrypt(plain_text):
    assert len(plain_text) == len(key)
    ciphertext = bytearray([a ^ b for a, b in zip(plain_text, key)])
    return ciphertext.hex()

print(encrypt(flag.encode("utf-8")))
print(encrypt(some_simple_text.encode("utf-8")))


# flag 65f32f851cdb20eee875eea5a9a30f826cfd247eb550dcc89d1d4cdf952f5c28ca5f162355567fd262bb96
# encrypted some_simple_text 70f8259330c137d4e873ff9ea6a559ab2dea1a60d943859aa545578395301d28a0741d1e065a24d45cb19f