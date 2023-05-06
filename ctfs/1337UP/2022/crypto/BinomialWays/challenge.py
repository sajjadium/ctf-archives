from secret import flag
val = []
flag_length = len(flag)
print(flag_length)

def factorial(n):
    f = 1
    for i in range(2, n+1):
        f *= i
    return f

def series(A, X, n):
    nFact = factorial(n)
    for i in range(0, n + 1):
        niFact = factorial(n - i)
        iFact = factorial(i)
        aPow = pow(A, n - i)
        xPow = pow(X, i)
        val.append(int((nFact * aPow * xPow) / (niFact * iFact)))

A = 1; X = 1; n = 30
series(A, X, n)
ct = []
for i in range(len(flag)):
    ct.append(chr(ord(flag[i])+val[i]%26))
print(''.join(ct))