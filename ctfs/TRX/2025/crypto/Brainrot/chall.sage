from Crypto.Util.number import bytes_to_long as b2l
flag = open("flag.txt", "r").read().strip()
assert flag.startswith("TRX{") and flag.endswith("}")
flag = flag[4:-1]
assert len(flag) == 40

def rot8000(s):
    news = ''
    for c in s:
        news += chr((ord(c) + 8000))
    return news

coeffs = [b2l(rot8000(flag[i:i+4]).encode('utf-16')) for i in range(0, len(flag), 4)]

def poly(x):
    return sum([c*x**i for i,c in enumerate(coeffs)]) % b2l(b'cant_give_you_everything')

points = [0xdeadbeef, 13371337, 0xcafebabe]

print([poly(p) % b2l(b'only_half!!!') for p in points])
# [25655763503777127809574173484, 8225698895190455994566939853, 10138657858525287519660632490]