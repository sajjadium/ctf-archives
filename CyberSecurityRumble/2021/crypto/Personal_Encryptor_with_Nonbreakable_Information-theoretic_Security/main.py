import os
import string
import hashlib

from flag import FLAG

# Check that flag wasn't corrupted
assert hashlib.sha256(FLAG.encode()).hexdigest() == \
    "59f03b531db63fe65b7b8522badee65488d7a63fd97c3134766faf3d0fde427c", "Flag Corrupt!"


ALPHABET = string.ascii_letters + "{}_!$&-%?()"


def keygen(length):
    key = ""
    rnd_bytes = os.urandom(length)
    for i in range(length):
        pos = rnd_bytes[i] % len(ALPHABET)
        key += ALPHABET[pos]
    return key


def encrypt(key, msg):
    assert len(key) == len(msg), "For Information-theoretic security the key needs to be as long as the msg."

    ciphertext = ""

    for i in range(len(msg)):
        msg_c = msg[i]
        key_c = key[i]

        if msg_c not in ALPHABET:
            ValueError(f"Can't encrypt char: {msg_c}")

        msg_pos_c = ALPHABET.index(msg_c)
        key_pos_c = ALPHABET.index(key_c)

        new_pos = (msg_pos_c + key_pos_c) % len(ALPHABET)
        ciphertext += ALPHABET[new_pos]

    return ciphertext

print("Welcome to our `Personal Encryptor with Nonbreakable Information-theoretic Security` DEMO.")
print("With this PoC we show our unbreakable cipher.")
print("Request as many ciphertexts as you want. You won't be able to decrypt!")
print("To encrypt own messages please buy the full version.")

inpt = int(input("How many ciphertexts would you like>"))
if 0 < inpt <= 1000:
    for _ in range(inpt):
        key = keygen(len(FLAG))
        print(encrypt(key, FLAG))
else:
    print("Please be reasonable.")

print("Thanks for trying our demo version. Good bye.")
