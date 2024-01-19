def PolynomialHash(s, a):
    return sum([ord(s[i]) * pow(a, len(s)-i-1) for i in range(len(s))])
 
flag = "***********"
PolynomialHash(flag, 256)

#35201194166317999524907401661096042001277