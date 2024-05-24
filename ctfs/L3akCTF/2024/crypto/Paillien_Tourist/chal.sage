from sage.all import *
from random import randint
from Crypto.Util.number import *

class Paillier:
    def __init__(self, bits):
        self.bits = bits
        self.pub, self.priv = self.keygen()

    def keygen(self):
        p = random_prime(2**self.bits)
        q = random_prime(2**self.bits)
        Lambda = (p - 1) * (q - 1)
        n = p * q
        Zn = IntegerModRing(n)
        Zn2 = IntegerModRing(n**2)
        g = Zn2(n + 1)
        mu = Zn(Lambda)**-1
        return ((n, g), (Lambda, mu))

    def encrypt(self, m):
        (n, g) = self.pub
        Zn2 = IntegerModRing(n**2)
        r = Zn2(randint(0, n))
        c = g**Zn2(m) * r**n
        return c

    def add(self, cipher_1, cipher_2):
        (n, g) = self.pub
        Zn2 = IntegerModRing(n**2)
        r = Zn2(randint(0, n))
        return cipher_1 * cipher_2 * r**n

    def sub(self, cipher_1, cipher_2):
        (n, g) = self.pub
        Zn2 = IntegerModRing(n**2)
        r = Zn2(randint(0, n))
        inv_cipher_2 = Zn2(cipher_2)**-1
        return cipher_1 * inv_cipher_2 * r**n

    def get_keys(self):
        return self.pub, self.priv

def toStr(msg):
    return long_to_bytes(int(msg))

# Generate key pairs
def main():
    paillier = Paillier(1024)
    pub_key, priv_key = paillier.get_keys()
    message_1 = randint(0, 420)
    cipher_1 = paillier.encrypt(message_1)
    message_2 = bytes_to_long(b"im so smrt, check me out mom")
    cipher_2 = paillier.encrypt(message_2)
    flag_message = bytes_to_long(b"L3AK{FAKE_FLAG_FAKE_FLAG}")
    flag_cipher = paillier.encrypt(flag_message)
    diff_cipher = paillier.sub(cipher_2, cipher_1)
    flag_cipher_modified = paillier.add(flag_cipher, diff_cipher)
    with open("challenge.txt", "w") as f:
        f.write(f"Ciphertext #1 = {hex(int(cipher_1))}\n")
        f.write(f"Ciphertext #2 = {hex(int(cipher_2))}\n")
        f.write(f"Modified Flag Cipher = {hex(int(flag_cipher_modified))}\n")
        f.write(f"Public Key = {hex(int(pub_key[0]))}, {hex(int(pub_key[1]))}\n")
        f.write(f"Private Key = {hex(int(priv_key[0]))}, {hex(int(priv_key[1]))}\n")
    

if __name__ == '__main__':
    main()