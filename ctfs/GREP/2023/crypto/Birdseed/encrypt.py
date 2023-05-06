import random
flag = open('flag.txt').read()

rand_seed = random.randint(0, 999)
random.seed(rand_seed)
encrypted = ''

for chr in flag:
    encrypted += f'{(ord(chr) ^ random.randint(0, 255)):02x}'

with open('out.txt', 'w') as f:
    f.write(encrypted)