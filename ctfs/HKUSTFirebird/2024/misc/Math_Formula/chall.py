from sage.all import *

# In case you don't want to install Sage, you can use https://sagecell.sagemath.org/ and I guarantee Sagemath Cell is sufficient in solving this challenge.
# Also, to someone who doesn't know about Sage, the QQ() below is just a wrapper for rational numbers so that it retains its exact value without the need to deal with float precision error.

flag = b'firebird{***REDACTED***}'

def f(n):
    return 1 + sum(floor(QQ((n, sum(floor(cos(QQ((factorial(j - 1) + 1, j)) * pi)**2) * (((-1)**(ceil(QQ(((j - 1), 2)))) + 1) // 2) for j in range(1, i + 1))))**QQ((1, n))) for i in range(1, 2**(n+2) + 1))

output = 1
for i in range(len(flag) - 2):
    output *= f(flag[i] * flag[i+1] * flag[i+2])
print(output)