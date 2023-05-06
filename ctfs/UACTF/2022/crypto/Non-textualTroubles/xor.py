from random import seed, randrange


seed(True, version=2)

with open("plaintext.txt", "r") as read, open("ciphertext.txt", "w") as write:
    plaintext = read.read()

    for char in plaintext:
        A = ord(char)
        B = randrange(256)
        ciphertext = chr(A ^ B)
        write.write(ciphertext)
