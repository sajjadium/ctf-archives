f = [x.strip() for x in open("chall.txt").read().split('\n')]
n = int(f[0])
a = list(map(int, f[1].split()))
m = 998244353

def factorial(n):
    if n==0: return 1
    if n==1: return 1
    return n * factorial(n-1)

def choose(n, r):
    return (factorial(n) // (factorial(r) * factorial(n-r))) % m

ans = 1
for x in a:
    ans *= choose(n, x)
    ans %= m
print(f"tjctf{{{ans}}}")