import os

class CrypTopiaSC:

    @staticmethod
    def KSA(key, n):
        S = list(range(n))
        j = 0
        for i in range(n):
            j = ((j + S[i] + key[i % len(key)]) >> 4 | (j - S[i] + key[i % len(key)]) << 4) & (n-1)
            S[i], S[j] = S[j], S[i]
        return S

    @staticmethod
    def PRGA(S, n):
        i = 0
        j = 0
        while True:
            i = (i+1) & (n-1)
            j = (j+S[i]) & (n-1)
            S[i], S[j] = S[j], S[i]
            yield S[((S[i] + S[j]) >> 4 | (S[i] - S[j]) << 4) & (n-1)]

    def __init__(self, key, n=256):
        self.KeyGenerator = self.PRGA(self.KSA(key, n), n)

    def encrypt(self, message):
        return bytes([char ^ next(self.KeyGenerator) for char in message])

def main():
    flag = b"XXX"
    key = os.urandom(256)
    encrypted_flag = CrypTopiaSC(key).encrypt(flag)
    print("Welcome to our first version of CrypTopia Stream Cipher!\nYou can here encrypt any message you want.")
    print(f"Oh, one last thing: {encrypted_flag.hex()}")
    while True:
        pt = input("Enter your message: ").encode()
        ct = CrypTopiaSC(key).encrypt(pt)
        print(ct.hex())

if __name__ == "__main__":
    main()