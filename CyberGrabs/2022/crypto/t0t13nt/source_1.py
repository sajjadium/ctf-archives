from sympy import totient

flag = REDACTED

def functor(n):
    val = 0
    for j in tqdm(range(1,n+1)):
        for i in range(1,j+1):
            val += j//i * totient(i)
    return val

lest = []
for i in flag:
    lest.append(functor(ord(i)*6969696969))

print(lest)


