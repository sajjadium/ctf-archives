from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
from Crypto.Cipher import AES
from random import randint, randbytes
from secrets import FLAG

class LayeredEncryption:
    def __init__(self, p, q, aes_key):
        assert len(aes_key) == 16
        self.n = p * q
        self.aes_key = aes_key
        self.e = 65537
        self.d = pow(self.e, -1, (p - 1) * (q - 1))

    def encrypt(self, m):
        iv = randbytes(16)
        aes_c = bytes_to_long(iv + AES.new(self.aes_key, AES.MODE_CBC, iv).encrypt(pad(m, 16)))

        print(aes_c)

        r = randint(1, 2**512 - 1)
        ri = pow(r, -1, self.n)
        return (r, pow(ri * aes_c, self.e, self.n), pow(ri * aes_c, self.d, self.n)) # salt, encrypted ciphertext, signature of ciphertext
        

    def decrypt(self, r, c, s):
        if r < 1 or r >= 2**512:
            print("Salt must a positive integer less than 2^512")
        elif c != pow(s, self.e * self.e, self.n):
            print("Signature is invalid!")
        else:
            aes_c_bytes = long_to_bytes((pow(c, self.d, self.n) * r) % self.n)
            iv, ciphertext = aes_c_bytes[:16], aes_c_bytes[16:]
            return unpad(AES.new(self.aes_key, AES.MODE_CBC, iv).decrypt(ciphertext), 16)


e = LayeredEncryption(getPrime(1024), getPrime(1024), randbytes(16))
r, c, s = e.encrypt(FLAG)
print(f"{e.n = }")
print(f"{e.e = }")
print("Welcome to my lair of layers!")
print(f"Foolish traveller! You think you can best all of my schemes!??! Here, a challenge: {(r, c, s)}")


while True:
    guess = input("Prithee, tell in a comma-separated triplet, what secret do i hold? ")
    try:
        if e.decrypt(*map(int, guess.split(","))) == FLAG:
            print("yes, AND IT SHALL NEVER SEE THE LIGHT OF DAY!")
        else:
            print("NAY!")
    except:
        print(f"what is bro doing 💀")
