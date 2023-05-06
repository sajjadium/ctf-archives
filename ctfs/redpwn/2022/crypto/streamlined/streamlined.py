import random

with open("aooo.txt", "r") as f:
    plaintext = f.read()
    
assert len(plaintext) == 14332

with open("flag.txt", "r") as f:
    flag = f.read()

assert len(flag) == 52 and flag.startswith("hope{") and flag.endswith("}")

plaintext = plaintext + flag
plaintext = plaintext.encode()

N = 8 * len(plaintext)

plaintext_bits = ["{:08b}".format(i) for i in plaintext]
plaintext_bits = "".join(plaintext_bits)
plaintext_bits = [int(i) for i in plaintext_bits]

key_bits = [random.randrange(2) for i in range(N // 5)] * (5 + 1)

ciphertext_bits = [i ^ j for i,j in zip(plaintext_bits, key_bits)]
ciphertext_string = ''.join([str(i) for i in ciphertext_bits])

with open("stream_output.txt", "w") as f:
    f.write(ciphertext_string)
