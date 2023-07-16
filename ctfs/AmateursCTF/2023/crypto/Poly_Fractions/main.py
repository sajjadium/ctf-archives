#!/usr/local/bin/python
import random
import math
from flag import flag, text

a = 1
b = random.randint(-10, 10)
b2 = random.randint(-10, 10)
numcoefficients = [a, b]
denomcoefficients = [a, b2]
query = 0
for i in flag:
    sign = random.randint(0, 1)
    if sign == 0:
        sign -= 1
    numcoefficients.append(sign * int(i))
for i in text:
    sign = random.randint(0, 1)
    if sign == 0:
        sign -= 1
    denomcoefficients.append(sign * int(i))
numcoefficients.reverse()
denomcoefficients.reverse()
while True:
    try:
        query += 1
        if query > 500:
            print("exceeded query limit!")
            exit(0)
        numcoefficients[-2] = random.randint(-10, 10)
        denomcoefficients[-2] = random.randint(-10, 10)
        x = int(input("x: "))
        if -99 <= x <= 99:
            x1 = 1
            numerator = 0
            for i in numcoefficients:
                numerator += i * x1
                x1 *= x
            x2 = 1
            denominator = 0
            for i in denomcoefficients:
                denominator += i * x2
                x2 *= x
            gcd = math.gcd(numerator, denominator)
            print(str(numerator//gcd) + "/" + str(denominator//gcd))
        else:
            print("input must be at most 2 digits")
    except:
        print("invalid input")
        exit(0)
