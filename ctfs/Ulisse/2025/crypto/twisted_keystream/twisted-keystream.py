import random
import os
from Crypto.Util.number import long_to_bytes,bytes_to_long
from base64 import b64encode
from wordfreq import word_frequency, top_n_list

FLAG = os.environ.get("FLAG","UlisseCTF{fakeflag}")
assert(FLAG[:10]=="UlisseCTF{")
assert(FLAG[-1]=="}")
assert(len(FLAG)<50)
block_size=16

def xor(a,b):
    return bytes([a ^ b for a,b in zip(a,b)])

def generate_weighted_words(n, top_n=500000):
    word_list = top_n_list("en", top_n)
    probabilities = [word_frequency(word, "en") for word in word_list]
    total = sum(probabilities)
    probabilities = [p / total for p in probabilities]
    sampled_words = random.choices(word_list, weights=probabilities, k=n)
    return sampled_words

n=10000
plaintext = generate_weighted_words(n)
flagpos=random.randint(10,n-10)
plaintext.insert(flagpos,FLAG)
plaintext = " ".join(plaintext).encode()
plaintext=plaintext[:(len(plaintext)//block_size)*block_size]

key=os.urandom(block_size)
ciphertext=b""
twist=key
for i in range(len(plaintext)//block_size):
    ciphertext+=xor(key,plaintext[block_size*i:block_size*(i+1)])
    key=bytes_to_long(key)
    key=[(key>>i2)&1 for i2 in range(block_size*8)]
    random.Random(twist).shuffle(key)
    key=sum([key[i2]<<i2 for i2 in range(block_size*8)])
    key=long_to_bytes(key)
    key=b"\x00"*(block_size-len(key))+key
print(b64encode(ciphertext).decode())



