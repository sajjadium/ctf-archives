import random
from secret import flag
from fractions import Fraction

def score(a,b):
    if abs(a-b)<1/2**10:
        # capping score to 1024 so you dont get extra lucky
        return Fraction(2**10)
    return Fraction(2**53,int(2**53*a)-int(2**53*b))

total_score = 0
for _ in range(2000):
    try:
        x = random.random()
        y = float(input('enter your guess:\n'))
        round_score = score(x,y)
        total_score+=float(round_score)
        print('total score: {:0.2f}, round score: {}'.format(
            total_score,round_score))
        if total_score>10**6:
            print(flag)
            exit(0)
    except:
        print('Error, exiting')
        exit(1)
else:
    print('Maybe better luck next time')

