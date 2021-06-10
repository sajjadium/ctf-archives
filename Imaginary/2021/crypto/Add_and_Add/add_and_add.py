import random

with open("flag.txt") as f:
    flag = f.read().strip().encode()

x = bytes([random.randrange(256)])
while flag:
    y = flag[:len(x)]
    flag = flag[len(x):]
    x += bytes([(a + b) % 256 for a, b in zip(x, y)])

with open("output.txt", "w") as f:
    f.write(x[1:].hex())
