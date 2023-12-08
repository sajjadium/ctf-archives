import random


class Shrek:
    def __init__(self):
        file = open("shrek.txt")
        self.parts = list(file.read().split())
        alphabet = ""
        for part in self.parts:
            for letter in part:
                if not letter in alphabet:
                    alphabet += letter
        self.alphabet = alphabet + " "
        self.generateKeys()


    def generateKeys(self):
        keys = []
        for _ in range(20):
            key = []
            for _ in range(random.randint(10, 30)):
                key.append(random.randrange(len(self.alphabet)))
            keys.append(key)

        self.keys = keys


    def generatePlainText(self):
        plainText = ""
        for _ in range(100):
            plainText += random.choice(self.parts)
            plainText += " "
        return plainText.strip()


    def encrypt(self, plainText):
        cipherText = [*plainText]
        for i,j in enumerate(cipherText):
            for key in self.keys:
                cipherText[i] = self.alphabet[(self.alphabet.index(j) + key[i % len(key)]) % len(self.alphabet)]
        return ''.join(cipherText)
