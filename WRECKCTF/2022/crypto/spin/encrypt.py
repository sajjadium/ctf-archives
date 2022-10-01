with open('flag.txt', 'r') as file:
    plaintext = file.read().strip()

def spin(c, key):
    return chr((ord(c) - ord('a') - key) % 26 + ord('a'))

ciphertext = ''.join(
    spin(c, 43) if 'a' <= c <= 'z' else c
    for c in plaintext
)

with open('ciphertext.txt', 'w+') as file:
    file.write(ciphertext)
