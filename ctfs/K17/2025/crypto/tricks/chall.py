from Crypto.Util.number import getStrongPrime, long_to_bytes, bytes_to_long
from random import randint
from secrets import FLAG

assert len(FLAG) == 32

class Paillier:
    # en.wikipedia.org/wiki/Paillier_cryptosystem
    def __init__(self, p, q):
        self.n = p * q
        self.n2 = pow(self.n, 2)
        self.l = (p - 1) * (q - 1)
        self.mu = pow(self.l, -1, self.n)
        self.g = self.n + 1
        self.L = lambda x : (x - 1) // self.n
        
    def encrypt(self, m):
        return (pow(randint(1, self.n - 1), self.n, self.n2) * pow(self.g, m, self.n2)) % self.n2
        
    def decrypt(self, c):
        return (self.L(pow(c, self.l, self.n2)) * self.mu) % self.n


paillier = Paillier(getStrongPrime(1024), getStrongPrime(1024))
print(f"{paillier.n = }")

print(paillier.encrypt(bytes_to_long(FLAG)))
print("a key property of paillier encryption/decryption is that its homomorphic between the additive/multiplicative on the plaintext/ciphertext space")
print("the ability to anonymously add, or combine, encrypted streams is incredibly useful, one such application being")
print("TRICKS!!!")
print("YOU")
print("CAN")
print("DO")
print("TRICKS!!!!")
print("LET'S SEEE IF YOU CAN DO TRIIIIIICKS!!!!!!!!!!!!!!!!!!!!!!!!")
tricks = {
    "cha cha left": lambda x : x + b"\x00", # e.g. pow(x, 256, self.n2)
    "wave your hands": lambda x : b"\\_/-\\_/" + x + b"\\_/-\\_/",
    "SAY IT THREE TIMES": lambda x : x + x + x
}
print(f"you can {', '.join(tricks.keys())}... yeah that's pretty much it actually")
    
while True:
    trick = input("Which trick do you want to show me? ")
    if trick not in tricks:
        print("I've never heard of that trick before")
        continue

    
    x = int(input("What's the encrypted message you'd like to perform the trick on? "))
    y = int(input("What's the encrypted result of the trick? "))
    if bytes_to_long(tricks[trick](long_to_bytes(paillier.decrypt(x)))) == paillier.decrypt(y):
        print("HOLY SMOKES WHAT A TRICK!!!!!")
    else:
        print("nup.")
