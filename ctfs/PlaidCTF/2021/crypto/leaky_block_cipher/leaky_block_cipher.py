import flag
import hashcash

import secrets
from Crypto.Cipher import AES

def gf128(a, b):
    a = int.from_bytes(a, byteorder="big")
    b = int.from_bytes(b, byteorder="big")
    R = 128
    P = sum(1 << x for x in [R, 7, 2, 1, 0])
    r = 0
    for i in range(R):
        if a & (1 << i):
            r ^= b << i
    for i in range(R)[::-1]:
        if r & (1 << (i+R)):
            r ^= P << i
    return r.to_bytes(16, byteorder="big")

def xor(a, b):
    return bytes(x^y for x,y in zip(a,b))

class LeakyBlockCipher:
    def __init__(self, key = None):
        if key is None:
            key = secrets.token_bytes(16)
        self.key = key
        self.aes = AES.new(key, AES.MODE_ECB)
        self.H = self.aes.encrypt(bytes(16))
    def encrypt(self, iv, data):
        assert len(iv) == 16
        assert len(data) % 16 == 0
        ivi = int.from_bytes(iv, "big")
        cip = bytes()
        tag = bytes(16)
        for i in range(0,len(data),16):
            cntr = ((ivi + i // 16 + 1) % 2**128).to_bytes(16, byteorder="big")
            block = data[i:i+16]
            enced = self.aes.encrypt(xor(cntr, block))
            cip += enced
            tag = xor(tag, enced)
            tag = gf128(tag, self.H)
        tag = xor(tag, self.aes.encrypt(iv))
        return cip, tag

def main():
    resource = secrets.token_hex(8)
    print(resource)
    token = input()
    assert hashcash.check(token.strip(), resource, bits=21)

    print("Thanks for helping me try to find this leak.")
    print("Here's a few rounds of the cipher for you to investigate.")
    print("")
    for _ in range(20):
        G = LeakyBlockCipher()
        iv = secrets.token_bytes(16)
        print("iv =", iv.hex())
        plaintext = bytes.fromhex(input("plaintext = "))
        assert len(plaintext) > 100
        cip, tag = G.encrypt(iv, plaintext)
        print("secure auth tag =", tag.hex())
        print("")
        enc_iv = G.aes.encrypt(iv).hex()
        print("Have you caught the drip?")
        print("It looks like ", enc_iv[:-1] + "X")
        guess = input("So what is X? ").strip()
        if guess == enc_iv[-1:]:
            print("Good.  Now just to check, do it again for me.")
        else:
            print("Sorry, the answer was", enc_iv[-1:])
            break
    else:
        print(flag.flag)

if __name__ == "__main__":
    main()