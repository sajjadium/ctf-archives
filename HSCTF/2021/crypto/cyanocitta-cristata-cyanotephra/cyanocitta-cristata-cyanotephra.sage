import random
var("x y")
flag = int(open('flag.txt','rb').read().hex(),16)
xs = [random.randint(1,256) for i in range(9)]
ys = [random.randint(1,256) for i in range(9)]
assert not any([xs[i]==ys[i] for i in range(9)])
c = [random.randint(1,2^64) for i in range(len(xs))]
f(x,y)=c[0]*x^2+c[1]*y^2+c[2]*x*y+c[3]*x+c[4]*y+c[5]
solns = [int(f(xs[i],ys[i])) for i in range(len(xs))]
print([(xs[i],ys[i],solns[i]) for i in range(9)])
a,b = random.randint(1,2^40),random.randint(1,2^40)
print(a,b)
print((int(f(a,b)))^^flag)
