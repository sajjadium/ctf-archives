import random

f = open("flag.txt", "r").read()
random.seed(random.randint(0, 1000))
l = list(f[:-1])
random.shuffle(l)
print(''.join(l))
