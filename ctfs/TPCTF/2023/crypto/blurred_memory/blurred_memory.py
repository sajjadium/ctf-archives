
from secret import flag

assert flag[:6] == 'TPCTF{' and flag[-1] == '}'
flag = flag[6:-1]

assert len(set(flag)) == len(flag)

xs = []
for i, c in enumerate(flag):
    xs += [ord(c)] * (i + 1)

p = 257
print('output =', [sum(pow(x, k, p) for x in xs) % p for k in range(1, len(xs) + 1)])
