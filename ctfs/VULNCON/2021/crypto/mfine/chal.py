import random

def encrypt(plaintext):
    ciphertext = ''
    for letter in plaintext:
        i = ALPHA.index(letter)
        c = (a*i + b) % m
        ciphertext += ALPHA[c]
    return ciphertext


ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ{}_ #"
m = len(ALPHA)
a = random.randrange(1, m)
b = random.randrange(1, m)

message = open("message.txt").read().replace('\n', '')
cipher = encrypt(message)

with open("cipher.txt", 'w') as f:
    for i in range(0,len(cipher),64):
        f.write( cipher[i:i+64]+'\n' )
