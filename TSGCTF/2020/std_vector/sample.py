import stdvec

l = stdvec.StdVec()

for i in range(1000):
    l.append(i)

for i in range(l.size()):
    l.set(i, l.get(i) + 1)

s = 0
for x in l:
    s += x

print(s, sum(range(1001))) 
