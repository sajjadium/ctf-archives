import random

def do_thing(a, b):
    return ((a << 1) & b) ^ ((a << 1) | b)

x = input("What's the password? ")
if len(x) != 25:
    print("WRONG!!!!!")
else:
    random.seed(997)
    k = [random.randint(0, 256) for _ in range(len(x))]
    a = { b: do_thing(ord(c), d) for (b, c), d in zip(enumerate(x), k) }
    b = list(range(len(x)))
    random.shuffle(b)
    c = [a[i] for i in b[::-1]]
    print(k)
    print(c)
    kn = [47, 123, 113, 232, 118, 98, 183, 183, 77, 64, 218, 223, 232, 82, 16, 72, 68, 191, 54, 116, 38, 151, 174, 234, 127]
    valid = len(list(filter(lambda s: kn[s[0]] == s[1], enumerate(c))))
    if valid == len(x):
        print("Password is correct! Flag:", x)
    else:
        print("WRONG!!!!!!")
