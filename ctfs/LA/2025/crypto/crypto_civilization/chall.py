#!/usr/local/bin/python3

import hashlib
import os
import binascii


# s is 16 bits long, 32 bit output
def PRG(s: bytes) -> bytes:
    assert len(s) == 2, "You're trying to cheat! Go to Crypto Prison!"
    s_int = int.from_bytes(s, byteorder="big")

    h = hashlib.new("sha3_256")
    h.update(s)

    out = h.digest()

    return out[:4]


def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    if len(bytes1) != len(bytes2):
        raise ValueError("Byte objects must be of the same length")

    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))


print("In Crypto Civilization, nobody commits the beef. 0 = chicken and 1 = beef.")
print(
    "Every day, Crypto Noobs have 1.5 seconds to do the commitment challenge. Exceptional performers will level up to Crypto Pro."
)
print("Can you level up to a Crypto Pro?")

number_correct = 0

for i in range(200):
    print(f"Crypto test #{i + 1}")

    # generate 32-bit value
    y = os.urandom(4)
    print(f"Here's y: {y.hex()}")

    print("What's your commitment (hex)?")

    com_hex = input("> ").encode()

    try:
        com = binascii.unhexlify(com_hex)
    except:
        print("You're trying to cheat! Go to Crypto Prison!")
        exit(0)

    assert len(com) == 4, "You're trying to cheat! Go to Crypto Prison!"

    choice = int.from_bytes(os.urandom(1), byteorder="big") & 1  # random bit

    if choice == 0:
        print("Did you commit the chicken? Show me (hex).")

    elif choice == 1:
        print("Did you commit the beef? Show me (hex).")

    decom_hex = input("> ").encode()

    try:
        decom = binascii.unhexlify(decom_hex)
    except:
        print("You're trying to cheat! Go to Crypto Prison!")
        exit(0)

    assert len(decom) == 2, "You're trying to cheat! Go to Crypto Prison!"

    if choice == 0:
        if PRG(decom) == com:
            print("Good work. See you tomorrow.")
            number_correct += 1
        else:
            print("Ouch. You don't want to keep doing that.")

    elif choice == 1:
        if xor_bytes(PRG(decom), y) == com:
            print("Good work. See you tomorrow.")
            number_correct += 1
        else:
            print("Ouch. You don't want to keep doing that.")

print(f"{number_correct}/200 trials passed")

if number_correct > 132:
    print("Congrats! You leveled up to a Crypto Pro! Here's your flag.")
    print(open("flag.txt", "r").read())
else:
    print("You messed up too many tasks. You go to Crypto Prison.")
