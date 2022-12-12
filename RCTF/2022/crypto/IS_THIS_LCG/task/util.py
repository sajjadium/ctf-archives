def mt2dec(X, n, m):
    x = 0
    for i in range(n):
        for j in range(n):
            x = x + int(X[i, j]) * (m ** (i * n + j))
    return x