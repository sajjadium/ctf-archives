import os
import random
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

def get_seed(size):
    return int(os.urandom(size).hex(), 16)

input_data = None
output_data = ""

seed = get_seed(4)
random.seed(seed)

old = "0123456789abcdef"
new = list(old)
random.shuffle(new)
new = ''.join(new)

with open("input.txt", "r") as in_file:
    input_data = in_file.read()

for alpha in input_data:
    encoded = (bytes(alpha.encode()).hex())
    output_data += new[old.index(encoded[0])]
    output_data += new[old.index(encoded[1])]
    
with open("output1.txt", "w") as f:
    print("{}".format(output_data), file=f)

key = RSA.generate(4096, e=3)
msg = "" #from output1.txt
ind = 280
flag = "nite{do_not_worry_this_is_a_fake_flag!!}"
msg = msg[:ind] + flag + msg[ind:]
m = bytes_to_long(msg.encode())

c = pow(m, key.e, key.n)

with open("output2.txt", "w") as f:
    print("n = {}".format(key.n), file=f)
    print("e = {}".format(key.e), file=f)
    print("c = {}".format(c), file=f)