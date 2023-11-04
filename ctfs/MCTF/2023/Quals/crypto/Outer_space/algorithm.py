import random
from string import ascii_lowercase, digits

FLAG = 'mctf{redacted}'

alphabet = digits + ascii_lowercase
encrypt_table = {i: v for i, v in enumerate(alphabet)}
decrypt_table = {v: i for i, v in enumerate(alphabet)}


def encrypt(index: int) -> str:
    return encrypt_table[index // 36] + encrypt_table[index % 36]


def decrypt(string: str) -> int:
    return decrypt_table[string[0]] * 36 + decrypt_table[string[1]]


output = [''] * 1295
pos = random.randint(0, 1295)

for char in FLAG:
    if char == '{':
        char = 'v'
    elif char == '}':
        char = 'w'

    output[pos] = char + encrypt_table[random.randint(0, 35)]
    pos = decrypt(output[pos])

for i, v in enumerate(output):
    if not v:
        output[i] = encrypt(random.randint(0, 1295))

if __name__ == '__main__':
    with open('hash.txt', 'w') as file:
        file.write(''.join(output))
