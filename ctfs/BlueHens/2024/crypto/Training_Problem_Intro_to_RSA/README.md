In [9]: p = getPrime(128)
In [10]: q = getPrime(128)
In [11]: N = p*q
In [12]: bytes_to_long(flag) < N
Out[12]: True
In [13]: print(pow(bytes_to_long(flag), 65537, N), N)

-ProfNinja
