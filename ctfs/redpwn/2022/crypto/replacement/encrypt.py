import random

with open('text.txt') as f:
    plaintext = f.read()

with open('flag.txt') as f:
    plaintext += '\n' + f.read()

characters = set(plaintext) - {'\n'}

shuffled = list(characters)
random.shuffle(shuffled)

replacement = dict(zip(characters, shuffled))

ciphertext = ''.join(replacement.get(c, c) for c in plaintext)

with open('output.txt', 'w') as f:
    f.write(ciphertext)
