import random
from random import randint
def reverseMe(p):
    random.seed(3211210)
    arr = ['j', 'b', 'c', 'd', '2', 'f', 'g', 'h', '1', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'y',
           'v', '3', '}', '{', '_']
    t = []
    for i in range(len(arr), 0, -1):
        l = randint(0, i-1)
        t.append(arr[l])
        arr.remove(arr[l])
        arr.reverse()
    for i in range(5):
        s = ''
        for j in range(5):
            s += t[5*i+j]
    o = ''
    for k in range(0, len(p)-1, 2):
        q1 = t.index(p[k])
        q2 = t.index(p[k+1])
        if q1 // 5 == q2 //5:
            o += t[(q1//5)*5 + ((q1+1)%5)]
            o += t[(q2//5)*5 + ((q2+1)%5)]
        elif q1 % 5 == q2 % 5:
            o += t[((q1//5 + 1) % 5 * 5) + (q1%5)]
            o += t[((q2//5 + 1) % 5 * 5) + (q2%5)]
        else:
            o += t[(q1//5)*5+(q2%5)]
            o += t[(q2//5)*5+(q1%5)]
    print(o)

if __name__ == '__main__':
    inp = "REDACTED"
    reverseMe(inp)