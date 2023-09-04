flag = open('./flag.txt', 'rb').read().strip()
m1 = int.from_bytes(flag[:len(flag)//2])
m2 = int.from_bytes(flag[len(flag)//2:])
n = m1 * m2
print(n)
