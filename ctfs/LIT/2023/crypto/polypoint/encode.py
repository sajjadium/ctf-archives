from secrets import SystemRandom

gen = SystemRandom()

with open("flag.txt", "rb") as f:
    flag = f.read().strip()

assert len(flag) == 76
c = int.from_bytes(flag)

poly = [c]
for _ in range(10):
    poly.append(gen.randrange(pow(10, 11), pow(10, 12)))

for _ in range(10):
    x = gen.randrange(pow(10, 11), pow(10, 12))
    v = 1
    y = 0
    for i in range(11):
        y += poly[i] * v
        v *= x
    print(f"({x},{y})")
