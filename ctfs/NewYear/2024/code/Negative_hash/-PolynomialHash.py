def PolynomialHash(string, a):
    result = 0
    l = len(string)
    for i in range(l):
        result += ord(string[i]) * ((-a) ** (l - i - 1))
    return result
 
flag = "****************"
PolynomialHash(flag, 100)