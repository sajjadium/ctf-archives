import Crypto.Util.number as cun
import Crypto.Random.random as crr
import Crypto.Util.Padding as cup
from Crypto.Cipher import AES
import os
import hashlib


class DiffieHellman:
    def __init__(self, p: int):
        self.p = p
        self.g = 8
        self.private_key = crr.getrandbits(128)

    def public_key(self) -> int:
        return pow(self.g, self.private_key, self.p)

    def shared_key(self, other_public_key: int) -> int:
        return pow(other_public_key, self.private_key, self.p)


def get_prime() -> int:
    p = int(input("Please help them choose p: "))
    q = int(
        input(
            "To prove your p isn't backdoored, "
            + "give me a large prime factor of (p - 1): "
        )
    )

    if (
        cun.size(q) > 128
        and p > q
        and (p - 1) % q == 0
        and cun.isPrime(q)
        and cun.isPrime(p)
    ):
        return p
    else:
        raise ValueError("Invalid prime")


def main():
    print("Note: Your session ends in 30 seconds")

    message = "My favorite food is " + os.urandom(32).hex()
    print("Alice wants to send Bob a secret message")

    p = get_prime()
    alice = DiffieHellman(p)
    bob = DiffieHellman(p)

    shared_key = bob.shared_key(alice.public_key())
    assert shared_key == alice.shared_key(bob.public_key())

    aes_key = hashlib.sha1(cun.long_to_bytes(shared_key)).digest()[:16]
    cipher = AES.new(aes_key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(cup.pad(message.encode(), 16))

    print("Here's their encrypted message: " + ciphertext.hex())

    guess = input("Decrypt it and I'll give you the flag: ")
    if guess == message:
        print("Congrats! Here's the flag: " + os.environ["FLAG"])
    else:
        print("That's wrong dingus")


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
