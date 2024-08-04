import random

n = 696969

a = []
for i in range(n):
    a.append(random.randint(0, n))
    a[i] -= a[i] % 2

print(' '.join(list(map(str, a))))

for turns in range(20):
    c = int(input())
    for i in range(n):
        a[i] = abs(c - a[i])

    if len(set(a)) == 1:
        print(open('/flag.txt', 'r').read())
        break
